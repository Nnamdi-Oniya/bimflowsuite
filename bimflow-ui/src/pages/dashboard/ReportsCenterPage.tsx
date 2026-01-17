import React, { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import { Search, Download, Eye, X, ChevronLeft, ChevronRight, FileText, Calendar, Clock, Filter } from "lucide-react";
import "../../assets/ReportsCenterPage.css";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

interface Report {
  id: number;
  type: string;
  title: string;
  date: string;
  format: string;
  size: string;
  downloads: number;
  lastViewed?: string;
  previewUrl: string;
}

const ReportsCenterPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("all");
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [numPages, setNumPages] = useState<number | null>(null);

  const reports: Report[] = [
    { id: 1, type: "Compliance", title: "BIM Execution Plan Compliance Report", date: "Nov 18, 2025", format: "PDF", size: "2.4 MB", downloads: 42, lastViewed: "2 hours ago", previewUrl: "/sample-reports/compliance.pdf" },
    { id: 2, type: "Cost", title: "5D Cost Estimation Summary", date: "Nov 17, 2025", format: "PDF + Excel", size: "1.8 MB", downloads: 89, previewUrl: "/sample-reports/cost.pdf" },
    { id: 3, type: "Clash", title: "Clash Detection BCF Report", date: "Nov 16, 2025", format: "BCF", size: "856 KB", downloads: 27, previewUrl: "/sample-reports/clash.pdf" },
    { id: 4, type: "Schedule", title: "4D Gantt Schedule Export", date: "Nov 15, 2025", format: "PDF", size: "1.2 MB", downloads: 156, previewUrl: "/sample-reports/gantt.pdf" },
    { id: 5, type: "Full", title: "Complete Project Status Report", date: "Nov 14, 2025", format: "PDF", size: "8.9 MB", downloads: 203, lastViewed: "Yesterday", previewUrl: "/sample-reports/full.pdf" },
  ];

  const filteredReports = reports.filter(report =>
    (report.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
     report.type.toLowerCase().includes(searchTerm.toLowerCase())) &&
    (filterType === "all" || report.type === filterType)
  );

  const openPreview = (report: Report) => {
    setSelectedReport(report);
    setPageNumber(1);
  };

  const closePreview = () => {
    setSelectedReport(null);
    setPageNumber(1);
    setNumPages(null);
  };

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };

  return (
    <div className="reports-center-clean">
      <div className="reports-header-clean">
        <div className="header-content">
          <h1>Reports Center</h1>
          <p>All your BIM reports in one place • Instant preview available</p>
        </div>
        <div className="status-badge">
          <FileText size={20} />
          <span>{filteredReports.length} Reports Available</span>
        </div>
      </div>

      <div className="controls">
        <div className="search-box">
          <Search size={20} />
          <input
            type="text"
            placeholder="Search reports..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="filter-box">
          <Filter size={18} />
          <select value={filterType} onChange={(e) => setFilterType(e.target.value)}>
            <option value="all">All Reports</option>
            <option value="Compliance">Compliance</option>
            <option value="Cost">Cost</option>
            <option value="Clash">Clash Detection</option>
            <option value="Schedule">Schedule</option>
            <option value="Full">Full Report</option>
          </select>
        </div>
      </div>

      <div className="reports-grid-clean">
        {filteredReports.map((report) => (
          <div key={report.id} className="report-card-clean" onClick={() => openPreview(report)}>
            <div className="card-header">
              <FileText size={48} className="icon" />
              <span className="type-tag">{report.type}</span>
            </div>
            <div className="card-body">
              <h3>{report.title}</h3>
              <div className="meta">
                <span><Calendar size={16} /> {report.date}</span>
                <span><Clock size={16} /> {report.format} • {report.size}</span>
              </div>
              <div className="stats">
                <span><Download size={16} /> {report.downloads} downloads</span>
                {report.lastViewed && <span>• Last viewed {report.lastViewed}</span>}
              </div>
            </div>
            <div className="card-footer">
              <button className="preview-btn">
                <Eye size={18} /> Preview Report
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* PDF Preview Modal */}
      {selectedReport && (
        <div className="modal-overlay" onClick={closePreview}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-top">
              <h2>{selectedReport.title}</h2>
              <button onClick={closePreview} className="close-modal"><X size={28} /></button>
            </div>
            <div className="modal-content">
              <Document file={selectedReport.previewUrl} onLoadSuccess={onDocumentLoadSuccess} loading="Loading PDF...">
                <Page pageNumber={pageNumber} width={820} />
              </Document>
            </div>
            <div className="modal-bottom">
              <div className="pagination">
                <button onClick={() => setPageNumber(prev => Math.max(1, prev - 1))} disabled={pageNumber <= 1}>
                  <ChevronLeft />
                </button>
                <span>Page {pageNumber} of {numPages || "..."}</span>
                <button onClick={() => setPageNumber(prev => Math.min(numPages || prev, prev + 1))} disabled={pageNumber >= (numPages || 1)}>
                  <ChevronRight />
                </button>
              </div>
              <a href={selectedReport.previewUrl} download className="download-btn">
                <Download size={18} /> Download {selectedReport.format}
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportsCenterPage;