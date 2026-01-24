// src/App.tsx – FULLY UPDATED WITH ALL NEW DASHBOARD PAGES + FIXES
import React, { Component, Suspense, type ReactNode, useEffect } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import "./App.css";

// Core Components
import Header from "./components/Header";
import HeroSection from "./components/HeroSection";
import ServicesSection from "./components/ServicesSection";
import HowWeWorkSection from "./components/HowWeWorkSection";
import ProjectsTestimonialsSection from "./components/ProjectsTestimonialsSection";
import CTANewsSection from "./components/CTANewsSection";
import Footer from "./components/Footer";

// Lazy-loaded Pages (Public)
const DemoPage = React.lazy(() => import("./pages/DemoPage"));
const GenerateModelPage = React.lazy(() => import("./pages/GenerateModelPage"));
const UploadIFCPage = React.lazy(() => import("./pages/UploadIFCPage"));           // Public /upload
const FeaturesPage = React.lazy(() => import("./pages/FeaturesPage"));
const AboutPage = React.lazy(() => import("./pages/AboutPage"));
const ProjectsPageLanding = React.lazy(() => import("./pages/ProjectsPage"));
const BlogPage = React.lazy(() => import("./pages/BlogPage"));
const ContactPage = React.lazy(() => import("./pages/ContactPage"));
const LoginPage = React.lazy(() => import("./pages/LoginPage"));
const BookDemoPage = React.lazy(() => import("./pages/BookDemoPage"));
const ForgotPasswordPage = React.lazy(() => import("./pages/ForgotPasswordPage"));

// Dashboard Layout & Pages
const DashboardLayout = React.lazy(() => import("./components/DashboardLayout"));
const DashboardOverview = React.lazy(() => import("./pages/dashboard/DashboardPage"));
const DashboardProjects = React.lazy(() => import("./pages/dashboard/ProjectsPage"));
const DashboardGenerate = React.lazy(() => import("./pages/dashboard/GenerateModelPage"));
const DashboardCompliance = React.lazy(() => import("./pages/dashboard/ComplianceChecksPage"));
const DashboardAnalytics = React.lazy(() => import("./pages/dashboard/AnalyticsPage"));
const DashboardTemplates = React.lazy(() => import("./pages/dashboard/TemplatesPage"));
const DashboardSettings = React.lazy(() => import("./pages/dashboard/SettingsPage"));
const DashboardProfile = React.lazy(() => import("./pages/dashboard/ProfilePage"));

// === NEW DASHBOARD PAGES (ALL IMPORTED) ===
const ApiAccessPage = React.lazy(() => import("./pages/dashboard/ApiAccessPage"));
const ClashDetectionPage = React.lazy(() => import("./pages/dashboard/ClashDetectionPage"));
const CostEstimationPage = React.lazy(() => import("./pages/dashboard/CostEstimationPage"));
const ReportsCenterPage = React.lazy(() => import("./pages/dashboard/ReportsCenterPage"));
const DashboardUploadIFCPage = React.lazy(() => import("./pages/dashboard/UploadIFCPage"));
const ProjectSchedulingPage = React.lazy(() => import("./pages/dashboard/ProjectSchedulingPage"));
const ScenarioManagerPage = React.lazy(() => import("./pages/dashboard/ScenarioManagerPage"));

// Error Boundary, ScrollToTop, LoadingFallback (unchanged)
interface ErrorBoundaryState { hasError: boolean; }
class ErrorBoundary extends Component<{ children: ReactNode }, ErrorBoundaryState> {
  constructor(props: { children: ReactNode }) { super(props); this.state = { hasError: false }; }
  static getDerivedStateFromError(): ErrorBoundaryState { return { hasError: true }; }
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void { console.error("App Error:", error, errorInfo); }
  render(): ReactNode {
    if (this.state.hasError) {
      return (
        <div style={{ padding: "2rem", textAlign: "center", background: "#f5f5f5", minHeight: "100vh" }}>
          <h2>Oops! Something went wrong.</h2>
          <p>Check the console for details.</p>
          <button onClick={() => window.location.reload()} style={{ background: "#F8780F", color: "white", border: "none", padding: "0.75rem 1.5rem", borderRadius: "8px", cursor: "pointer", fontSize: "1rem", marginTop: "1rem" }}>
            Reload Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

const ScrollToTop: React.FC = () => {
  const { pathname } = useLocation();
  useEffect(() => {
    setTimeout(() => window.scrollTo({ top: 0, behavior: "smooth" }), 80);
  }, [pathname]);
  return null;
};

const LoadingFallback: React.FC = () => (
  <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "50vh", fontSize: "1.2rem", color: "#F8780F" }}>
    Loading...
  </div>
);

const AppContent: React.FC = () => {
  const location = useLocation();
  const isDashboard = location.pathname.startsWith("/dashboard");
  const hideFooterPaths = ["/login", "/book-demo", "/forgot-password"];
  const showFooter = !isDashboard && !hideFooterPaths.includes(location.pathname);

  return (
    <div className="app-container">
      {!isDashboard && <Header />}
      <ScrollToTop />

      <main className="main-content">
        <Suspense fallback={<LoadingFallback />}>
          <Routes>
            {/* HOME */}
            <Route path="/" element={
              <>
                <HeroSection />
                <ServicesSection />
                <HowWeWorkSection />
                <ProjectsTestimonialsSection />
                <CTANewsSection />
              </>
            } />

            {/* PUBLIC PAGES */}
            <Route path="/demo" element={<DemoPage />} />
            <Route path="/generate-model" element={<GenerateModelPage />} />
            <Route path="/upload" element={<UploadIFCPage />} />
            <Route path="/features" element={<FeaturesPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/projects" element={<ProjectsPageLanding />} />
            <Route path="/blog" element={<BlogPage />} />
            <Route path="/contact" element={<ContactPage />} />

            {/* AUTH */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/book-demo" element={<BookDemoPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />

            {/* DASHBOARD – ALL NEW PAGES ADDED */}
            <Route path="/dashboard" element={<DashboardLayout />}>
              <Route index element={<DashboardOverview />} />
              <Route path="projects" element={<DashboardProjects />} />
              <Route path="generate" element={<DashboardGenerate />} />
              <Route path="compliance" element={<DashboardCompliance />} />
              <Route path="analytics" element={<DashboardAnalytics />} />
              <Route path="templates" element={<DashboardTemplates />} />
              <Route path="settings" element={<DashboardSettings />} />
              <Route path="profile" element={<DashboardProfile />} />

              {/* === NEW ROUTES === */}
              <Route path="api" element={<ApiAccessPage />} />
              <Route path="clash-detection" element={<ClashDetectionPage />} />
              <Route path="cost-estimation" element={<CostEstimationPage />} />
              <Route path="reports" element={<ReportsCenterPage />} />
              <Route path="upload-ifc" element={<DashboardUploadIFCPage />} />
              <Route path="scheduling" element={<ProjectSchedulingPage />} />
              <Route path="scenarios" element={<ScenarioManagerPage />} />
            </Route>

            {/* 404 */}
            <Route path="*" element={
              <div style={{ padding: "4rem 2rem", textAlign: "center", minHeight: "50vh", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
                <h1 style={{ fontSize: "3rem", fontWeight: 800 }}>404</h1>
                <p style={{ fontSize: "1.2rem", maxWidth: "450px" }}>The page you are looking for does not exist.</p>
                <a href="/" style={{ marginTop: "1.5rem", color: "#F8780F", border: "2px solid #F8780F", padding: "0.75rem 1.5rem", borderRadius: "8px", textDecoration: "none" }}>
                  Return Home
                </a>
              </div>
            } />
          </Routes>
        </Suspense>
      </main>

      {!isDashboard && showFooter && <Footer />}
    </div>
  );
};

const App: React.FC = () => (
  <ErrorBoundary>
    <AppContent />
  </ErrorBoundary>
);

export default App;