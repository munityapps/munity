import logo from '../../assets/logo.png';
import { ProgressSpinner } from 'primereact/progressspinner';

const LoadingMunity = () => {
	return <div className="app-loading">
		<img src={logo} alt="Logo" />
		<ProgressSpinner />
	</div>;
}

export default LoadingMunity;