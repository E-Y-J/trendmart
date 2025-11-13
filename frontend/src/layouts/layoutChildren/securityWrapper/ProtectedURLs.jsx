import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { checkAuthStatus } from '../../../redux/auth/authSlice';
import { Outlet, useNavigate } from 'react-router-dom';

function ProtectedURLs() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { isAuthenticated, status } = useSelector((state) => state.auth);

  useEffect(() => {
    // Runs once on mount, verifies session
    dispatch(checkAuthStatus());
  }, [dispatch]);

  useEffect(() => {
    // If checkAuthStatus fails, redirect to login
    if (status === 'failed' || (!isAuthenticated && status !== 'loading')) {
      navigate('/login');
    }
  }, [isAuthenticated, status, navigate]);

  // Optional: show loading screen while verifying session
  if (status === 'loading') {
    return <div className="text-center mt-5">Checking session...</div>;
  }

  // Authenticated users can access nested routes
  return <Outlet />;
}

export default ProtectedURLs;
