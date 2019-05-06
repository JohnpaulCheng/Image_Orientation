from image_utils import angleCal, create_images, plot_result_bar

rotate_angle = 5
mode = "SIFT"

result_orig, result_rotate, result_rotate_translation,\
result_perspective, result_correction = create_images(rotate_angle)

name_result = []
result = []

for i in range(3):
    if i == 0:
        mode = "SIFT"
    elif i == 1:
        mode = "ORB"
    else:
        mode = "SURF"
    print("-----The Descriptor {0:s} is using-----".format(mode))
    # Rotate
    mean_rotate, time = angleCal(result_orig, result_rotate, mode)
    result.append(mean_rotate), name_result.append(mode + "R")
    print("Rotate: {0:6.3f} in {1:.3f}".format(mean_rotate, time))

    # Rotate and Translation
    mean_rotate_translation, time = angleCal(result_orig, result_rotate_translation, mode)
    result.append(mean_rotate_translation), name_result.append(mode + "T+R")
    print("Rotate and translation: {0:6.3f} in {1:.3f}".format(mean_rotate_translation, time))

    # Perspective
    mean_perspective, time = angleCal(result_orig, result_perspective, mode)
    result.append(mean_perspective), name_result.append(mode + "P")
    print("Perspective: {0:6.3f} in {1:.3f}".format(mean_perspective, time))

    # Correction
    mean_correction, time = angleCal(result_orig, result_correction, mode)
    result.append(mean_correction), name_result.append(mode + "C")
    print("Correction: {0:6.3f} in {1:.3f}".format(mean_correction, time))

plot_result_bar(name_result, result, rotate_angle)


