import { useState } from 'react'
import './App.css'

function App() {
  const [selectedColor, setSelectedColor] = useState('black')
  const [quantity, setQuantity] = useState(1)
  const [isAddedToCart, setIsAddedToCart] = useState(false)

  const colors = [
    { id: 'black', name: 'Midnight Black', hex: '#1a1a1a' },
    { id: 'silver', name: 'Platinum Silver', hex: '#e8e8e8' },
    { id: 'gold', name: 'Rose Gold', hex: '#b76e79' },
    { id: 'blue', name: 'Ocean Blue', hex: '#2c3e50' }
  ]

  const features = [
    { icon: 'fa-solid fa-gem', title: 'Sapphire Crystal', description: 'Scratch-resistant sapphire crystal glass' },
    { icon: 'fa-solid fa-water', title: 'Water Resistant', description: 'Up to 100 meters / 330 feet' },
    { icon: 'fa-solid fa-battery-full', title: 'Long Battery', description: 'Up to 5 years battery life' },
    { icon: 'fa-solid fa-shield-alt', title: '5-Year Warranty', description: 'Comprehensive manufacturer warranty' }
  ]

  const incrementQuantity = () => setQuantity(quantity + 1)
  const decrementQuantity = () => {
    if (quantity > 1) setQuantity(quantity - 1)
  }

  const handleAddToCart = () => {
    setIsAddedToCart(true)
    setTimeout(() => setIsAddedToCart(false), 3000)
  }

  return (
    <div className="app">
      {/* Hero Section */}
      <header className="hero-section">
        <div className="container">
          <nav className="navbar">
            <div className="logo">CHRONOS</div>
            <div className="nav-links">
              <a href="#features">Features</a>
              <a href="#gallery">Gallery</a>
              <a href="#specs">Specifications</a>
              <a href="#contact">Contact</a>
            </div>
            <div className="cart-icon">
              <i className="fas fa-shopping-bag"></i>
              <span className="cart-count">0</span>
            </div>
          </nav>

          <div className="hero-content">
            <div className="hero-text">
              <span className="product-tag">NEW COLLECTION</span>
              <h1 className="product-title">Aether Chronograph</h1>
              <p className="product-subtitle">
                Experience timeless elegance with our premium Swiss-made chronograph. 
                Precision engineering meets minimalist design.
              </p>
              <div className="price-section">
                <span className="price">$2,499</span>
                <span className="original-price">$2,999</span>
                <span className="discount">Save 17%</span>
              </div>
              <button className="cta-button" onClick={handleAddToCart}>
                {isAddedToCart ? (
                  <>
                    <i className="fas fa-check"></i> Added to Cart
                  </>
                ) : (
                  <>
                    <i className="fas fa-shopping-cart"></i> Add to Cart
                  </>
                )}
              </button>
            </div>
            
            <div className="hero-image">
              <div className={`watch-display ${selectedColor}`}>
                <div className="watch-face">
                  <div className="watch-dial">
                    <div className="watch-hands"></div>
                    <div className="watch-markers"></div>
                  </div>
                </div>
                <div className="watch-strap"></div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Color Selection */}
      <section className="color-section">
        <div className="container">
          <h2 className="section-title">Select Your Style</h2>
          <p className="section-subtitle">Choose from our premium finishes</p>
          
          <div className="color-options">
            {colors.map(color => (
              <div 
                key={color.id}
                className={`color-option ${selectedColor === color.id ? 'selected' : ''}`}
                onClick={() => setSelectedColor(color.id)}
              >
                <div 
                  className="color-swatch" 
                  style={{ backgroundColor: color.hex }}
                ></div>
                <span className="color-name">{color.name}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features-section" id="features">
        <div className="container">
          <h2 className="section-title">Crafted for Excellence</h2>
          <p className="section-subtitle">Every detail matters in our pursuit of perfection</p>
          
          <div className="features-grid">
            {features.map((feature, index) => (
              <div className="feature-card" key={index}>
                <div className="feature-icon">
                  <i className={feature.icon}></i>
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quantity & Details */}
      <section className="details-section">
        <div className="container">
          <div className="details-grid">
            <div className="quantity-selector">
              <h3 className="details-title">Quantity</h3>
              <div className="quantity-controls">
                <button className="qty-btn" onClick={decrementQuantity}>
                  <i className="fas fa-minus"></i>
                </button>
                <span className="quantity-display">{quantity}</span>
                <button className="qty-btn" onClick={incrementQuantity}>
                  <i className="fas fa-plus"></i>
                </button>
              </div>
              <p className="stock-info">
                <i className="fas fa-check-circle"></i> In stock • Free shipping
              </p>
            </div>

            <div className="specs-list">
              <h3 className="details-title">Specifications</h3>
              <ul>
                <li><strong>Movement:</strong> Swiss automatic chronograph</li>
                <li><strong>Case:</strong> 42mm stainless steel</li>
                <li><strong>Crystal:</strong> Sapphire, anti-reflective coating</li>
                <li><strong>Water Resistance:</strong> 100m / 330ft</li>
                <li><strong>Strap:</strong> Genuine leather with quick-release</li>
                <li><strong>Warranty:</strong> 5 years international</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="testimonials-section">
        <div className="container">
          <h2 className="section-title">Loved by Connoisseurs</h2>
          <div className="testimonials-grid">
            <div className="testimonial-card">
              <div className="testimonial-content">
                <p>"The attention to detail is remarkable. This watch has become my daily companion."</p>
              </div>
              <div className="testimonial-author">
                <div className="author-avatar">JD</div>
                <div className="author-info">
                  <h4>James Donovan</h4>
                  <span>Watch Collector</span>
                </div>
              </div>
            </div>

            <div className="testimonial-card">
              <div className="testimonial-content">
                <p>"Perfect balance of classic design and modern functionality. Exceeds expectations."</p>
              </div>
              <div className="testimonial-author">
                <div className="author-avatar">SR</div>
                <div className="author-info">
                  <h4>Sarah Roberts</h4>
                  <span>Luxury Editor</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="app-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-brand">
              <div className="logo">CHRONOS</div>
              <p className="footer-tagline">Timeless elegance, engineered for life.</p>
            </div>
            
            <div className="footer-links">
              <div className="link-group">
                <h4>Product</h4>
                <a href="#features">Features</a>
                <a href="#specs">Specifications</a>
                <a href="#gallery">Gallery</a>
              </div>
              
              <div className="link-group">
                <h4>Support</h4>
                <a href="#contact">Contact Us</a>
                <a href="#faq">FAQ</a>
                <a href="#warranty">Warranty</a>
              </div>
              
              <div className="link-group">
                <h4>Legal</h4>
                <a href="#privacy">Privacy Policy</a>
                <a href="#terms">Terms of Service</a>
                <a href="#returns">Return Policy</a>
              </div>
            </div>
          </div>
          
          <div className="footer-bottom">
            <p>© 2024 Chronos Luxury Watches. All rights reserved.</p>
            <div className="social-links">
              <a href="#instagram"><i className="fab fa-instagram"></i></a>
              <a href="#twitter"><i className="fab fa-twitter"></i></a>
              <a href="#facebook"><i className="fab fa-facebook-f"></i></a>
              <a href="#pinterest"><i className="fab fa-pinterest"></i></a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
