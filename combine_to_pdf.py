# Modified version of https://github.com/GekySan/SushiScan-DLer/blob/main/convert_to_pdf.py

from PIL import Image
import os
from natsort import natsorted

def main_combine(chapter_dir=None):
    root_folder = os.path.join(os.path.dirname(__file__),'outputs')

    if chapter_dir :
        folder_to_convert = chapter_dir
    else :
        root_subfolders = [f.path for f in os.scandir(root_folder) if f.is_dir() and not f.path.endswith('PDF')]

        for a in range(len(root_subfolders)):
            print(f'{a} - {root_subfolders[a]}')

        index_to_convert = input("Please enter the number for the folder to convert: ")
        folder_to_convert = root_subfolders[int(index_to_convert)]
    
    main_folder_path = os.path.join(root_folder, folder_to_convert)

    if not os.path.exists(main_folder_path):
        print(f"The folder '{main_folder_path}' does not exist.")
        exit()

    combine_folder(work_dir=main_folder_path)

def combine_folder(work_dir : str) :
    subfolders = [f.path for f in os.scandir(work_dir) if f.is_dir()]

    if not subfolders:
        print("No subfolders found in the main folder.\nTrying to use main folder as subfolder.")
        combine_subfolder(work_dir)
        exit()

    for subfolder in subfolders:
        combine_subfolder(subfolder)

def combine_subfolder(chap_dir : str):
    chap_dir = os.path.normpath(chap_dir)
    root_dir = os.path.join(chap_dir.split('outputs', 1)[0], 'outputs')
    work_name = chap_dir.split('\\')[-2]
    subfolder_name = os.path.basename(chap_dir)

    image_files = [f for f in os.listdir(chap_dir) if os.path.isfile(os.path.join(chap_dir, f))]
    image_files = natsorted(image_files)

    if not image_files:
        print(f"No images found in the subfolder '{subfolder_name}'.")
        raise ValueError('No images in subfolder')

    first_image = Image.open(os.path.join(chap_dir, image_files[0]))

    other_images = [Image.open(os.path.join(chap_dir, image)).convert('RGB') for image in image_files[1:]]

    output_folder = os.path.join(root_dir, work_name + " - PDF")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_pdf_path = os.path.join(output_folder, f"{subfolder_name}.pdf")
    first_image.save(output_pdf_path, save_all=True, append_images=other_images)
    print(f"Images from subfolder '{subfolder_name}' have been merged into '{output_pdf_path}'.")

    first_image.close()
    for img in other_images:
        img.close()

if __name__ == '__main__':
    main_combine()