import appConstants from '../constants/appConstants';
import imageConstants from '../constants/imageConstants'

export const fetchResults = (directory) => (dispatch) => {
	const url = appConstants.RESULTS + '/' + directory;
	return fetch(url, {method: 'GET'})
		.then((response) => response.json())
		.then((response) => {
			dispatch(resultSuccess(response))
		}).catch((error) => {
			console.log(error)
			alert('Some error occurred.')
	})
}

const resultSuccess = (payload) => ({
	type: imageConstants.RESULTS_SUCCESS,
	payload
})
