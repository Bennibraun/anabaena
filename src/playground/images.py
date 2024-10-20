from nd2reader import ND2Reader
import matplotlib.pyplot as plt

# Open the first .nd2 file and load the first image
with ND2Reader('/Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20210709_Ana_-N_to_-N_channelbf,cy5,cfp,rfp_seq0000_0000.nd2') as images1:
    image1 = images1[0]  # Accessing the first image

# Open the second .nd2 file and load the first image
with ND2Reader('/Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB002/2.nd2') as images2:
    image2 = images2[0]  # Accessing the first image

# Plot the two images side by side
plt.figure(figsize=(10, 5))

# Display the first image
plt.subplot(1, 2, 1)
plt.imshow(image1, cmap='gray')  # Assuming the image is grayscale; change cmap for color images
plt.title('Image 1')
plt.axis('off')

# Display the second image
plt.subplot(1, 2, 2)
plt.imshow(image2, cmap='gray')  # Assuming the image is grayscale; change cmap for color images
plt.title('Image 2')
plt.axis('off')

# Show the plot
plt.tight_layout()
plt.savefig("/Users/zaca2954/academics/anabaena/src/playground/images.png")
plt.show()
