import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/dashboard';
import { useParams } from 'react-router-dom';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/dashboard/:stateName" element={<DashboardWrapper />} />
      </Routes>
    </Router>
  );
}

// Wrap with URL param handling
const DashboardWrapper: React.FC = () => {
  const { stateName } = useParams<{ stateName: string }>();
  return stateName ? <Dashboard stateName={stateName} /> : <div>Loading...</div>;
};

export default App;