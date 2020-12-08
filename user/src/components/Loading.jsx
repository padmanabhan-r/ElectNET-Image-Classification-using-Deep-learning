import React, { Component } from 'react';
import loader  from '../images/loader.gif';
import '../styles/app.css'

class Loading extends Component {

	componentDidMount() {
		this.props.fetchResults(this.props.imageUploader.directory)
	}

	componentWillUpdate(nextProps) {
		if(nextProps.results.result_success) {
			this.props.history.push('/result')
		}
	}

	render() {
		return (
			<div className="app-container">
				<div className="loader-icon"><img src={loader} alt="Calculating your results ..." /></div>
				<p className="loader-text">Classifying your image(s)</p>
			</div>
		);
	}
}

export default Loading;
