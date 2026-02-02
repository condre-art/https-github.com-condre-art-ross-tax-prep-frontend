import { render, screen } from '@testing-library/react';
import React from 'react';
import App from './App';

test('renders app heading', () => {
  render(<App />);
  expect(screen.getByText(/eROS Tax Preparation Platform/i)).toBeInTheDocument();
});

test('renders badges certificates and licenses sections', () => {
  render(<App />);
  expect(screen.getByText(/Badges/i)).toBeInTheDocument();
  expect(screen.getByText(/IRS Authorized e-File Provider/i)).toBeInTheDocument();
  expect(screen.getByText(/Certificates/i)).toBeInTheDocument();
  expect(screen.getByText(/Licenses/i)).toBeInTheDocument();
  expect(screen.getByText(/PTIN Active/i)).toBeInTheDocument();
});
