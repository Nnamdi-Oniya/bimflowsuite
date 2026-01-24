import React, { useState } from "react";
import "../assets/BlogPage.css";
import blogHero from "../assets/images/blog-hero.jpg";
import blogTutorial from "../assets/images/blog-tutorial.jpg";
import digitalConstruction from "../assets/images/DigitalConstruction.jpg";
import bimWorkflow from "../assets/images/BIMWorkflow.jpg";
import infrastructure from "../assets/images/Infrastructure.jpg";
import compliance from "../assets/images/Compliance.jpg";
import smeTrends from "../assets/images/SMETrends.jpg";
import openSourceBIM from "../assets/images/OpenSourceBIM.jpg";

const BlogPage: React.FC = () => {
  const [activeCategory, setActiveCategory] = useState<string>("all");
  const categories = [
    { id: "all", label: "All Posts" },
    { id: "tutorials", label: "Tutorials" },
    { id: "industry", label: "Industry News" },
    { id: "case-studies", label: "Case Studies" },
    { id: "technical", label: "Technical" }
  ];

  const blogPosts = [
    {
      id: 1,
      category: "tutorials",
      title: "Getting Started with BIMFlow Suite: A Complete Guide",
      excerpt: "Learn how to create your first BIM model using intent-driven modeling. This comprehensive guide covers everything from installation to your first project.",
      author: "Nnamdi Oniya",
      date: "November 15, 2025",
      readTime: "8 min read",
      image: blogTutorial,
      tags: ["Beginner", "Tutorial", "Getting Started"]
    },
    {
      id: 2,
      category: "industry",
      title: "The Future of BIM: Open Standards and SME Adoption",
      excerpt: "Exploring how open-source BIM tools are democratizing digital construction and enabling SMEs to compete in the modern construction landscape.",
      author: "Engineering Team",
      date: "November 10, 2025",
      readTime: "6 min read",
      image: digitalConstruction,
      tags: ["Industry", "Open Source", "Trends"]
    },
    {
      id: 3,
      category: "case-studies",
      title: "How SME Contractors Reduced Project Time by 40%",
      excerpt: "Real-world case study of a UK construction firm that automated their BIM workflow using BIMFlow Suite, achieving significant time and cost savings.",
      author: "Success Stories",
      date: "November 5, 2025",
      readTime: "10 min read",
      image: bimWorkflow,
      tags: ["Case Study", "ROI", "Success Story"]
    },
    {
      id: 4,
      category: "technical",
      title: "Understanding IFC 4.3: What's New for Infrastructure",
      excerpt: "Deep dive into IFC 4.3 standards and how BIMFlow Suite leverages these for multi-asset support across buildings, bridges, and roads.",
      author: "Technical Team",
      date: "October 28, 2025",
      readTime: "12 min read",
      image: infrastructure,
      tags: ["IFC", "Standards", "Infrastructure"]
    },
    {
      id: 5,
      category: "tutorials",
      title: "Automated Compliance Checking: Step-by-Step Guide",
      excerpt: "Master the compliance engine with this detailed tutorial on setting up rule packs and running automated validation checks on your BIM models.",
      author: "Nnamdi Oniya",
      date: "October 20, 2025",
      readTime: "15 min read",
      image: compliance,
      tags: ["Compliance", "Tutorial", "Automation"]
    },
    {
      id: 6,
      category: "industry",
      title: "BIM Adoption Trends in 2025: What SMEs Need to Know",
      excerpt: "Analysis of current BIM adoption rates, barriers facing SMEs, and how open-source solutions are changing the game.",
      author: "Industry Insights",
      date: "October 12, 2025",
      readTime: "7 min read",
      image: smeTrends,
      tags: ["Trends", "SME", "Market Analysis"]
    },
    {
      id: 7,
      category: "case-studies",
      title: "Open Source BIM: Revolutionizing Construction Workflows",
      excerpt: "Case study on how open-source BIM tools like BIMFlow Suite are transforming traditional construction processes for global teams.",
      author: "Case Studies Team",
      date: "October 5, 2025",
      readTime: "9 min read",
      image: openSourceBIM,
      tags: ["Open Source", "Case Study", "Workflow"]
    }
  ];

  const filteredPosts = activeCategory === "all" 
    ? blogPosts 
    : blogPosts.filter(p => p.category === activeCategory);

  const featuredPost = blogPosts[0];

  return (
    <div className="app-container">
      
      <main className="main-content" role="main">
        <div className="blog-page">
          {/* Hero Section with Background Image */}
          <section 
            className="blog-hero"
            style={{
              backgroundImage: `linear-gradient(rgba(78, 68, 60, 0.6), rgba(42, 36, 32, 0.6)), url(${blogHero})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundAttachment: 'fixed'
            }}
          >
            <div className="blog-hero__overlay"></div>
            <div className="blog-hero__content">
              <div className="hero-badge">
                <span className="badge-icon">📝</span>
                <span>Insights & Tutorials</span>
              </div>
              <h1 className="blog-hero__title">
                BIMFlow Suite Blog
              </h1>
              <p className="blog-hero__subtitle">
                Expert insights, tutorials, and industry news about BIM automation, 
                digital construction, and open-source innovation.
              </p>
            </div>
          </section>

          {/* Featured Post */}
          <section className="featured-post-section">
            <div className="section-container">
              <h2 className="section-label">Featured Article</h2>
              <div className="featured-post">
                <div className="featured-post__image-wrapper">
                  <img 
                    src={featuredPost.image} 
                    alt={featuredPost.title}
                    className="featured-post__image"
                  />
                  <div className="featured-badge">⭐ Featured</div>
                </div>
                <div className="featured-post__content">
                  <div className="post-meta">
                    <span className="post-category">{featuredPost.category}</span>
                    <span className="post-date">{featuredPost.date}</span>
                    <span className="post-read-time">⏱️ {featuredPost.readTime}</span>
                  </div>
                  <h2 className="featured-post__title">{featuredPost.title}</h2>
                  <p className="featured-post__excerpt">{featuredPost.excerpt}</p>
                  <div className="featured-post__footer">
                    <div className="post-author">
                      <div className="author-avatar">👤</div>
                      <span className="author-name">{featuredPost.author}</span>
                    </div>
                    <button className="read-more-btn">
                      Read Article →
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Category Filter */}
          <section className="category-filter-section">
            <div className="section-container">
              <div className="category-filters">
                {categories.map((cat) => (
                  <button
                    key={cat.id}
                    className={`category-btn ${activeCategory === cat.id ? 'category-btn--active' : ''}`}
                    onClick={() => setActiveCategory(cat.id)}
                  >
                    {cat.label}
                  </button>
                ))}
              </div>
            </div>
          </section>

          {/* Blog Posts Grid */}
          <section className="blog-posts-section">
            <div className="section-container">
              <div className="blog-posts-grid">
                {filteredPosts.slice(1).map((post) => (
                  <article key={post.id} className="blog-post-card">
                    <div className="blog-post-card__image-wrapper">
                      <img 
                        src={post.image} 
                        alt={post.title}
                        className="blog-post-card__image"
                      />
                      <span className="post-category-badge">{post.category}</span>
                    </div>
                    <div className="blog-post-card__content">
                      <div className="post-meta">
                        <span className="post-date">{post.date}</span>
                        <span className="post-read-time">⏱️ {post.readTime}</span>
                      </div>
                      <h3 className="blog-post-card__title">{post.title}</h3>
                      <p className="blog-post-card__excerpt">{post.excerpt}</p>
                      <div className="blog-post-card__tags">
                        {post.tags.map((tag, index) => (
                          <span key={index} className="post-tag">{tag}</span>
                        ))}
                      </div>
                      <div className="blog-post-card__footer">
                        <div className="post-author-small">
                          <span className="author-icon">👤</span>
                          <span>{post.author}</span>
                        </div>
                        <button className="read-link">Read More →</button>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            </div>
          </section>

          {/* Newsletter CTA */}
          <section className="newsletter-section">
            <div className="newsletter-container">
              <div className="newsletter-content">
                <h2 className="newsletter-title">Stay Updated</h2>
                <p className="newsletter-text">
                  Get the latest BIM insights, tutorials, and industry news delivered 
                  to your inbox. Join 1,000+ construction professionals.
                </p>
                <form className="newsletter-form">
                  <input 
                    type="email" 
                    placeholder="Enter your email address"
                    className="newsletter-input"
                  />
                  <button type="submit" className="newsletter-btn">
                    Subscribe
                  </button>
                </form>
                <p className="newsletter-privacy">
                  We respect your privacy. Unsubscribe anytime.
                </p>
              </div>
            </div>
          </section>
        </div>
      </main>
     
    </div>
  );
};

export default BlogPage;