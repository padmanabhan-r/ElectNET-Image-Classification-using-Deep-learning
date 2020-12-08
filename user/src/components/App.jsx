import React, { Component } from 'react';
import ImageUploader  from './ImageUploader';
import '../styles/app.css'

class App extends Component {

	render() {
		return (
			<div className="app-container">
				<p className="app-description">Upload your file to get the category it belongs to.</p>
				<ImageUploader {...this.props}/>
			</div>
		);
	}
}

export default App;
