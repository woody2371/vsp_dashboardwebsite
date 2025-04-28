import { jsx as _jsx } from "react/jsx-runtime";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/dashboard';
import { useParams } from 'react-router-dom';
function App() {
    return (_jsx(Router, { children: _jsx(Routes, { children: _jsx(Route, { path: "/dashboard/:stateName", element: _jsx(DashboardWrapper, {}) }) }) }));
}
// Wrap with URL param handling
const DashboardWrapper = () => {
    const { stateName } = useParams();
    return stateName ? _jsx(Dashboard, { stateName: stateName }) : _jsx("div", { children: "Loading..." });
};
export default App;
