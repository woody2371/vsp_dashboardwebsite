import { BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import Dashboard from './pages/dashboard';
import { useParams } from 'react-router-dom';
import IgnoredOrders from './pages/ignored_orders';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard/wa" replace />} />
        <Route path="/dashboard/:stateName" element={<DashboardWrapper />} />
        <Route path="/ignored_orders/:stateName" element={<IgnoredOrdersWrapper />} />
      </Routes>
    </Router>
  );
}

// Wrap with URL param handling
const DashboardWrapper: React.FC = () => {
  const { stateName } = useParams<{ stateName: string }>();
  return stateName ? <Dashboard stateName={stateName} /> : <div>Loading...</div>;
};

const IgnoredOrdersWrapper: React.FC = () => {
  const { stateName } = useParams<{ stateName: string }>();
  return stateName ? <IgnoredOrders stateName={stateName} /> : <div>Loading...</div>;
};

export default App;