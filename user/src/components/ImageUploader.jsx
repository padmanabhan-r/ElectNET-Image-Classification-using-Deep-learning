import React, { Component } from 'react';
import { FilePond, registerPlugin } from 'react-filepond';
import 'filepond/dist/filepond.min.css';
import appConstants from '../constants/appConstants'
import FilePondPluginFileValidateSize from 'filepond-plugin-file-validate-size';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview';
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css';
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type';

registerPlugin(FilePondPluginImagePreview, FilePondPluginFileValidateSize, FilePondPluginFileValidateType)

class ImageUploader extends Component {

	fileProgress = (file, progress) => {
		if(progress === 1) {
			this.props.history.push('/loading')
		}
	}
	
	render() {
		return (
			<div>
				<FilePond 
					className="image-uploader"
					onupdatefiles={this.onChange}
					server={
						{
							url: appConstants.SERVER,
							process: {
								onload: (res) => {
									this.props.insertDirectory(JSON.parse(res).directory)
								}
							}
						}
					}
					onprocessfileprogress={this.fileProgress}
					allowFileSizeValidation={true}
					maxFileSize="25MB"
					allowFileTypeValidation={true}
					acceptedFileTypes={['image/jpeg']}
				/>
			</div>
		);
	}
}

export default ImageUploader;
