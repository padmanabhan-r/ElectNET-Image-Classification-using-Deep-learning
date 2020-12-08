import imageConstants from '../constants/imageConstants'

export const insertDirectory = (directory) => ({
	type: imageConstants.DIRECTORY_UPLOAD,
	directory
})


