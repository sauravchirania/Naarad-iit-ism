import dropbox

class Uploader:
    def connect_to_server(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)
        self.dbx.users_get_current_account()

    def upload_file(self, file_name, file_address):
        with open(file_address, 'rb') as fp:
            f = fp.read()
            print('Opened file: ', file_name)
            uploaded_file_metadata \
                = self.dbx.files_upload(f, '/' + file_name, autorename=True)
            print('Uploaded the file ', file_name)
            file_url = uploaded_file_metadata.path_display
            sharing_data = self.dbx.sharing_create_shared_link(file_url)
            idx = sharing_data.url.rfind('?')
            download_link = sharing_data.url[:idx] + '?dl=1'
            return download_link
