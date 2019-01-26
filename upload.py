#https://developers.google.com/photos/library/guides/upload-media

    def upload(service, file):
        f = open(file, 'rb').read();

        url = 'https://photoslibrary.googleapis.com/v1/uploads'
        headers = {
            'Authorization': "Bearer " + service._http.request.credentials.access_token,
            'Content-Type': 'application/octet-stream',
            'X-Goog-Upload-File-Name': file,
            'X-Goog-Upload-Protocol': "raw",
        }

        r = requests.post(url, data=f, headers=headers)
        print '\nUpload token: %s' % r.content
        return r.content

    def createItem(service, upload_token, albumId):
        url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'

        body = {
            'newMediaItems' : [
                {
                    "description": "test upload",
                    "simpleMediaItem": {
                        "uploadToken": upload_token
                    }
                }
            ]
        }

        if albumId is not None:
            body['albumId'] = albumId;

        bodySerialized = json.dumps(body);
        headers = {
            'Authorization': "Bearer " + service._http.request.credentials.access_token,
            'Content-Type': 'application/json',
        }

        r = requests.post(url, data=bodySerialized, headers=headers)
        print '\nCreate item response: %s' % r.content
        return r.content;

//authenticate user and build service
upload_token = upload(service, './path_to_image.png')
response = createItem(service,upload_token, album['id'])
