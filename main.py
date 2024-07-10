import itk
import vtk
from vtk.util import numpy_support
import numpy as np

def load_scan(file_path):
    image = itk.imread(file_path, itk.F)
    return image

def register_images(fixed_image, moving_image):
    Dimension = 3

    FixedImageType = itk.Image[itk.F, Dimension]
    MovingImageType = itk.Image[itk.F, Dimension]

    TransformType = itk.VersorRigid3DTransform[itk.D]

    OptimizerType = itk.RegularStepGradientDescentOptimizerv4[itk.D]

    MetricType = itk.MeanSquaresImageToImageMetricv4[FixedImageType, MovingImageType]

    RegistrationType = itk.ImageRegistrationMethodv4[FixedImageType, MovingImageType]

    transform = TransformType.New()
    optimizer = OptimizerType.New()

    metric = MetricType.New()

    registration = RegistrationType.New()

    initializer = itk.CenteredTransformInitializer[TransformType, FixedImageType, MovingImageType].New(Transform=transform, FixedImage=fixed_image, MovingImage=moving_image)

    initializer.InitializeTransform()

    registration.SetFixedImage(fixed_image)
    registration.SetMovingImage(moving_image)
    registration.SetMetric(metric)
    registration.SetOptimizer(optimizer)
    registration.SetInitialTransform(transform)
    registration.SetNumberOfLevels(1)
    registration.Update()

    resampler = itk.ResampleImageFilter.New(Input=moving_image, Transform=registration.GetTransform(), UseReferenceImage=True, ReferenceImage=fixed_image)
    resampler.SetDefaultPixelValue(0)
    resampler.Update()

    registered_image = resampler.GetOutput()
    
    return registered_image

def segment_tumor(image):
    image_array = itk.GetArrayViewFromImage(image)

    if np.all(image_array == image_array.flat[0]):
        raise ValueError("Image contains uniform pixel values. Segmentation cannot be performed.")
    
    otsu_filter = itk.OtsuThresholdImageFilter.New(Input=image)
    otsu_filter.Update()
    threshold_value = otsu_filter.GetThreshold()

    binary_threshold = itk.BinaryThresholdImageFilter.New(Input=image)
    binary_threshold.SetLowerThreshold(threshold_value)
    binary_threshold.SetUpperThreshold(itk.NumericTraits[itk.F].max())
    binary_threshold.SetInsideValue(1)
    binary_threshold.SetOutsideValue(0)
    binary_threshold.Update()

    segmented_image = binary_threshold.GetOutput()

    return segmented_image

def visualize_changes(image1, image2):
    subtract_filter = itk.SubtractImageFilter.New(Input1=image1, Input2=image2)
    subtract_filter.Update()

    abs_filter = itk.AbsImageFilter.New(Input=subtract_filter.GetOutput())
    abs_filter.Update()

    diff = abs_filter.GetOutput()
    diff_np = itk.GetArrayFromImage(diff)

    dims = diff.GetLargestPossibleRegion().GetSize()

    vtk_image_data = vtk.vtkImageData()
    vtk_image_data.SetDimensions(dims[0], dims[1], dims[2])
    vtk_image_data.AllocateScalars(vtk.VTK_FLOAT, 1)

    vtk_data_array = numpy_support.numpy_to_vtk(num_array=diff_np.ravel(), deep=True, array_type=vtk.VTK_FLOAT)

    vtk_image_data.GetPointData().SetScalars(vtk_data_array)

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(vtk_image_data)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    renderer.AddActor(actor)
    renderer.SetBackground(1, 1, 1)
    render_window.Render()
    render_window_interactor.Start()

def main():
    scan1_path = 'Data/case6_gre1.nrrd'
    scan2_path = 'Data/case6_gre2.nrrd'

    scan1 = load_scan(scan1_path)
    scan2 = load_scan(scan2_path)

    registered_scan2 = register_images(scan1, scan2)

    segmented_tumor1 = segment_tumor(scan1)
    segmented_tumor2 = segment_tumor(registered_scan2)

    visualize_changes(segmented_tumor1, segmented_tumor2)

if __name__ == "__main__":
    main()
