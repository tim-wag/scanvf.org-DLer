# Modified version of https://github.com/GekySan/SushiScan-DLer/blob/main/convert_to_pdf.py

from PIL import Image
import os
from natsort import natsorted

def main_combine(chapter_dir=None, output_dir=None, to_scan_dir=None):
    if not output_dir :
        output_dir = os.path.join(os.path.dirname(__file__),'outputs')

    if not to_scan_dir: 
        to_scan_dir = os.path.join(os.path.dirname(__file__),'outputs')
    
    if chapter_dir :
        folder_to_convert = chapter_dir
    else :
        root_subfolders = [f.path for f in os.scandir(to_scan_dir) if f.is_dir() and not f.path.endswith('PDF')]

        for a in range(len(root_subfolders)):
            print(f'{a} - {root_subfolders[a]}')

        index_to_convert = input("Please enter the number for the folder to convert: ")
        folder_to_convert = root_subfolders[int(index_to_convert)]
    
    main_folder_path = os.path.join(to_scan_dir, folder_to_convert)

    if not os.path.exists(main_folder_path):
        print(f"The folder '{main_folder_path}' does not exist.")
        exit()

    combine_folder(folder_dir=main_folder_path, output_dir=output_dir)

def combine_folder(folder_dir : str, output_dir=None) :
    subfolders = [f.path for f in os.scandir(folder_dir) if f.is_dir()]

    if not subfolders:
        print("No subfolders found in the main folder.\nTrying to use main folder as subfolder.")
        combine_subfolder(folder_dir, output_dir)
        exit()

    for subfolder in subfolders:
        combine_subfolder(subfolder, output_dir)

def combine_subfolder(chap_dir : str, output_dir=None):
    chap_dir = os.path.normpath(chap_dir)
    if not output_dir :
        output_dir = os.path.join(chap_dir.split('outputs', 1)[0], 'outputs')
    work_name = chap_dir.split('\\')[-2]
    subfolder_name = os.path.basename(chap_dir)

    image_files = [f for f in os.listdir(chap_dir) if os.path.isfile(os.path.join(chap_dir, f))]
    image_files = natsorted(image_files)

    if not image_files:
        print(f"No images found in the subfolder '{subfolder_name}'.")
        raise ValueError('No images in subfolder')

    first_image = Image.open(os.path.join(chap_dir, image_files[0]))

    other_images = [Image.open(os.path.join(chap_dir, image)).convert('RGB') for image in image_files[1:]]

    output_dir = os.path.join(output_dir, work_name + " - PDF")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_pdf_path = os.path.join(output_dir, f"{subfolder_name}.pdf")
    first_image.save(output_pdf_path, save_all=True, append_images=other_images)
    print(f"Images from subfolder '{subfolder_name}' have been merged into '{output_pdf_path}'.")

    first_image.close()
    for img in other_images:
        img.close()

if __name__ == '__main__':
    main_combine()