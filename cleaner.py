import os

import shutil



async def delete_files(*files):


    for file in files:


        try:

            if not file:
                continue


            # File Delete

            if os.path.isfile(file):

                os.remove(file)


            # Folder Delete

            elif os.path.isdir(file):

                shutil.rmtree(

                    file,

                    ignore_errors=True

                )

        except:
            pass



async def clean_temp_folder():

    temp_folder = "temp"


    if not os.path.exists(
        temp_folder
    ):

        return


    for item in os.listdir(
        temp_folder
    ):

        path = os.path.join(

            temp_folder,

            item

        )


        try:

            if os.path.isfile(path):

                os.remove(path)


            elif os.path.isdir(path):

                shutil.rmtree(

                    path,

                    ignore_errors=True

                )

        except:
            pass