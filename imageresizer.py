from PIL import Image

def resize_image(input_img,output_img,size):
    orignal=Image.open(input_img)
    resized_img=orignal.resize(size)
    resized_img.save(output_img)
    print(f'Image saved as {output_img}')


input_img = './cat.jpg'
output_img = 'output.jpg'
new_size=(200,200)

resize_image(input_img=input_img,output_img=output_img,size=new_size)