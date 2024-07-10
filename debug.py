import itk
import vtk
from vtk.util import numpy_support

def load_scan(file_path):
    image = itk.imread(file_path, itk.F)
    return image

def convert_itk_to_vtk(itk_image):
    np_image = itk.GetArrayFromImage(itk_image)
    dims = itk_image.GetLargestPossibleRegion().GetSize()
    
    vtk_image_data = vtk.vtkImageData()
    vtk_image_data.SetDimensions(dims[0], dims[1], dims[2])
    vtk_image_data.AllocateScalars(vtk.VTK_FLOAT, 1)
    
    vtk_data_array = numpy_support.numpy_to_vtk(num_array=np_image.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
    vtk_image_data.GetPointData().SetScalars(vtk_data_array)
    
    return vtk_image_data

def apply_lookup_table(mapper):
    lookup_table = vtk.vtkLookupTable()
    lookup_table.SetRange(0, 255)
    lookup_table.Build()
    
    mapper.SetLookupTable(lookup_table)
    mapper.SetColorModeToMapScalars()
    mapper.SetScalarRange(0, 255)

def visualize_images(image1, image2):
    vtk_image1 = convert_itk_to_vtk(image1)
    vtk_image2 = convert_itk_to_vtk(image2)
    
    mapper1 = vtk.vtkDataSetMapper()
    mapper1.SetInputData(vtk_image1)

    apply_lookup_table(mapper1)

    actor1 = vtk.vtkActor()
    actor1.SetMapper(mapper1)
    
    mapper2 = vtk.vtkDataSetMapper()
    mapper2.SetInputData(vtk_image2)

    apply_lookup_table(mapper2)

    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)
    
    renderer1 = vtk.vtkRenderer()
    renderer2 = vtk.vtkRenderer()
    
    renderer1.SetViewport(0.0, 0.0, 0.5, 1.0)
    renderer2.SetViewport(0.5, 0.0, 1.0, 1.0)
    
    renderer1.AddActor(actor1)
    renderer2.AddActor(actor2)
    
    renderer1.SetBackground(1, 1, 1)
    renderer2.SetBackground(1, 1, 1)
    
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer1)
    render_window.AddRenderer(renderer2)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    
    render_window.Render()
    render_window_interactor.Start()

def main():
    scan1_path = 'Data/case6_gre1.nrrd'
    scan2_path = 'Data/case6_gre2.nrrd'

    scan1 = load_scan(scan1_path)
    scan2 = load_scan(scan2_path)
    
    visualize_images(scan1, scan2)

if __name__ == "__main__":
    main()
