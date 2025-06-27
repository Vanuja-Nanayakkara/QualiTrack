// src/pages/dashboard.tsx
import React from "react";
import { ProtectedRoute } from "../components/auth/ProtectedRoute";
import { useAuth } from "../contexts/AuthContext";

const Dashboard = () => {
  const { currentUser } = useAuth();

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 pt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-4 text-gray-600">
            Welcome, {currentUser?.email}! You are now signed in to your
            account.
          </p>

          {/* Add your dashboard content here */}
          <div className="mt-8 bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900">
              Your Quality Inspection Dashboard
            </h2>
            <p className="mt-2 text-gray-600">
              This is where you&apos;ll see your quality inspection data and
              metrics.
            </p>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default Dashboard;
