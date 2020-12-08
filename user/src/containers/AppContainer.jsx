import React, { Component } from 'react';
import { connect } from 'react-redux';
import App from '../components/App'

import { insertDirectory } from '../actions/imageUploadActions'

class AppContainer extends Component {
	render() {
		return (
			<App {...this.props} />
		)
	}
}

const mapStateToProps = (state) => state

const mapDispatchToProps = (dispatch) => ({

	insertDirectory: (directory) => {
		dispatch(insertDirectory(directory))
	}

})
export default connect(mapStateToProps, mapDispatchToProps)(AppContainer);