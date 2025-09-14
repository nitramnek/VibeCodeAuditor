import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../contexts/AuthContext';
import Layout from './Layout';
import TopBar from './TopBar';
import SideBar from './SideBar';
import MobileNav from './MobileNav';

// Mock components for testing
const MockAuthProvider = ({ children }) => (
  <div data-testid="auth-provider">{children}</div>
);

const TestWrapper = ({ children }) => (
  <BrowserRouter>
    <MockAuthProvider>
      {children}
    </MockAuthProvider>
  </BrowserRouter>
);

describe('Layout Components', () => {
  describe('TopBar', () => {
    test('renders logo and navigation elements', () => {
      render(
        <TestWrapper>
          <TopBar onMenuClick={() => {}} isMobile={false} />
        </TestWrapper>
      );
      
      expect(screen.getByText('VibeCodeAuditor')).toBeInTheDocument();
      expect(screen.getByText('Enterprise Security Platform')).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/Search scans, issues/)).toBeInTheDocument();
    });

    test('shows mobile menu button on mobile', () => {
      render(
        <TestWrapper>
          <TopBar onMenuClick={() => {}} isMobile={true} />
        </TestWrapper>
      );
      
      expect(screen.getByLabelText('Open sidebar')).toBeInTheDocument();
    });

    test('handles search focus and blur', () => {
      render(
        <TestWrapper>
          <TopBar onMenuClick={() => {}} isMobile={false} />
        </TestWrapper>
      );
      
      const searchInput = screen.getByPlaceholderText(/Search scans, issues/);
      fireEvent.focus(searchInput);
      
      expect(screen.getByText('Recent Searches')).toBeInTheDocument();
    });
  });

  describe('SideBar', () => {
    test('renders navigation items', () => {
      render(
        <TestWrapper>
          <SideBar />
        </TestWrapper>
      );
      
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Security Scanner')).toBeInTheDocument();
      expect(screen.getByText('Scan Results')).toBeInTheDocument();
      expect(screen.getByText('Compliance')).toBeInTheDocument();
      expect(screen.getByText('Analytics')).toBeInTheDocument();
    });

    test('shows quick stats', () => {
      render(
        <TestWrapper>
          <SideBar />
        </TestWrapper>
      );
      
      expect(screen.getByText('Quick Overview')).toBeInTheDocument();
      expect(screen.getByText('Active Scans')).toBeInTheDocument();
      expect(screen.getByText('Critical Issues')).toBeInTheDocument();
      expect(screen.getByText('Resolved')).toBeInTheDocument();
    });

    test('displays enterprise plan information', () => {
      render(
        <TestWrapper>
          <SideBar />
        </TestWrapper>
      );
      
      expect(screen.getByText('Enterprise Plan')).toBeInTheDocument();
      expect(screen.getByText('Unlimited scans & compliance')).toBeInTheDocument();
    });
  });

  describe('MobileNav', () => {
    test('renders mobile navigation with close button', () => {
      const mockOnClose = jest.fn();
      
      render(
        <TestWrapper>
          <MobileNav onClose={mockOnClose} />
        </TestWrapper>
      );
      
      expect(screen.getByText('VibeCodeAuditor')).toBeInTheDocument();
      
      const closeButton = screen.getByRole('button');
      fireEvent.click(closeButton);
      expect(mockOnClose).toHaveBeenCalled();
    });

    test('shows mobile-optimized quick stats', () => {
      render(
        <TestWrapper>
          <MobileNav onClose={() => {}} />
        </TestWrapper>
      );
      
      expect(screen.getByText('Quick Overview')).toBeInTheDocument();
      expect(screen.getByText('Active Scans')).toBeInTheDocument();
      expect(screen.getByText('Critical Issues')).toBeInTheDocument();
      expect(screen.getByText('Resolved Today')).toBeInTheDocument();
    });
  });

  describe('Layout', () => {
    test('renders children content', () => {
      render(
        <TestWrapper>
          <Layout>
            <div data-testid="test-content">Test Content</div>
          </Layout>
        </TestWrapper>
      );
      
      expect(screen.getByTestId('test-content')).toBeInTheDocument();
    });

    test('handles responsive behavior', () => {
      // Mock window.innerWidth
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 768,
      });

      render(
        <TestWrapper>
          <Layout>
            <div>Content</div>
          </Layout>
        </TestWrapper>
      );

      // Trigger resize event
      window.innerWidth = 1024;
      fireEvent(window, new Event('resize'));
      
      // Layout should adapt to desktop view
      expect(screen.getByText('VibeCodeAuditor')).toBeInTheDocument();
    });
  });
});

// Performance test utilities
export const measureLayoutPerformance = () => {
  const startTime = performance.now();
  
  return {
    end: () => {
      const endTime = performance.now();
      return endTime - startTime;
    }
  };
};

// Accessibility test utilities
export const checkAccessibility = async (component) => {
  const { container } = render(component);
  
  // Check for proper ARIA labels
  const buttons = container.querySelectorAll('button');
  buttons.forEach(button => {
    expect(button).toHaveAttribute('aria-label');
  });
  
  // Check for proper heading hierarchy
  const headings = container.querySelectorAll('h1, h2, h3, h4, h5, h6');
  expect(headings.length).toBeGreaterThan(0);
  
  // Check for proper focus management
  const focusableElements = container.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  expect(focusableElements.length).toBeGreaterThan(0);
};

export default {
  measureLayoutPerformance,
  checkAccessibility
};