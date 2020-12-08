import imageConstants from '../constants/imageConstants'

const initialState = {
	directory: '1543227241.13445'
}

export default (state = initialState, action={}) => {
	switch (action.type) {
		case imageConstants.DIRECTORY_UPLOAD:
			return {
				...state,
				...{
					directory: action.directory
				}
			}
		default:
			return state
	}
}