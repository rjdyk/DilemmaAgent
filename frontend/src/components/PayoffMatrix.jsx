// src/components/PayoffMatrix.js
import React from 'react';

function PayoffMatrix() {
  return (
    <div className="mb-4">
      <h2 className="text-lg font-semibold mb-2">The payoffs in a one-on-one game are:</h2>
      <table className="border-collapse border">
        <thead>
          <tr>
            <th className="border p-2"></th>
            <th className="border p-2">Cooperate</th>
            <th className="border p-2">Cheat</th>
          </tr>
        </thead>
        <tbody>
          {/* Add matrix values */}
        </tbody>
      </table>
    </div>
  );
}

export default PayoffMatrix;