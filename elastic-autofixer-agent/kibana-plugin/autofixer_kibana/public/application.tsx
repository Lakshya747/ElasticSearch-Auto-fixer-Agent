import React from 'react';
import ReactDOM from 'react-dom';
import { MainDashboard } from './components/MainDashboard';

export const renderApp = (element: HTMLElement) => {
  ReactDOM.render(<MainDashboard />, element);
  return () => ReactDOM.unmountComponentAtNode(element);
};