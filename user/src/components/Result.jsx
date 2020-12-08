import React, { Component } from 'react';
import ResultItem  from './ResultItem';
import '../styles/app.css';

class Result extends Component {

	renderResultItems = () => {
		return this.props.results.result_data.map((image, index) => {
			return <ResultItem key={index} {...image} />
		})
	}

	uploadAnotherClick = () => {
		this.props.history.push('/')
	}

	render() {
		return (
			<div className="result-container">
				<div className="sections">{this.renderResultItems()}</div>
				<p className="upload-another">Click <span className="upload-another-link" onClick={this.uploadAnotherClick}>here</span> to upload another image.</p>
			</div>
		);
	}
}

export default Result;
