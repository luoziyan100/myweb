// Mobile Menu Toggle
const menuBtn = document.querySelector('.menu-btn');
const navLinks = document.querySelector('.nav-links');

if (menuBtn) {
    menuBtn.addEventListener('click', () => {
        menuBtn.classList.toggle('open');
        navLinks.classList.toggle('open');
    });
}

// Close mobile menu when clicking on a nav link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        if (menuBtn.classList.contains('open')) {
            menuBtn.classList.remove('open');
            navLinks.classList.remove('open');
        }
    });
});

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Back to top button
const backToTopBtn = document.getElementById('back-to-top-btn');
if (backToTopBtn) {
    backToTopBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Show/hide back to top button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopBtn.style.opacity = '1';
            backToTopBtn.style.visibility = 'visible';
        } else {
            backToTopBtn.style.opacity = '0';
            backToTopBtn.style.visibility = 'hidden';
        }
    });
}

// Particles.js config
if (document.getElementById('particles-js')) {
    particlesJS('particles-js', {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": {
                "value": "#ffffff"
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                },
                "polygon": {
                    "nb_sides": 5
                }
            },
            "opacity": {
                "value": 0.3,
                "random": false,
                "anim": {
                    "enable": false,
                    "speed": 1,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 3,
                "random": true,
                "anim": {
                    "enable": false,
                    "speed": 40,
                    "size_min": 0.1,
                    "sync": false
                }
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#4e9af1",
                "opacity": 0.2,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 2,
                "direction": "none",
                "random": false,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
                "attract": {
                    "enable": false,
                    "rotateX": 600,
                    "rotateY": 1200
                }
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "grab"
                },
                "onclick": {
                    "enable": true,
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 140,
                    "line_linked": {
                        "opacity": 0.6
                    }
                },
                "bubble": {
                    "distance": 400,
                    "size": 40,
                    "duration": 2,
                    "opacity": 8,
                    "speed": 3
                },
                "repulse": {
                    "distance": 200,
                    "duration": 0.4
                },
                "push": {
                    "particles_nb": 4
                },
                "remove": {
                    "particles_nb": 2
                }
            }
        },
        "retina_detect": true
    });
}

// Neural Network Visualization
const neuralNetworkCanvas = document.getElementById('neural-network');
if (neuralNetworkCanvas) {
    const ctx = neuralNetworkCanvas.getContext('2d');
    let width, height;
    let nodes = [];
    let connections = [];
    let animatedPoints = [];
    
    // Colors
    const colors = {
        node: '#4e9af1',
        nodeStroke: '#6c3ce9',
        connection: 'rgba(78, 154, 241, 0.2)',
        point: '#fff'
    };
    
    // Node class
    class Node {
        constructor(x, y, radius) {
            this.x = x;
            this.y = y;
            this.radius = radius;
            this.originalRadius = radius;
            this.hovered = false;
        }
        
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = colors.node;
            ctx.fill();
            ctx.strokeStyle = colors.nodeStroke;
            ctx.lineWidth = 2;
            ctx.stroke();
        }
        
        update() {
            if (this.hovered && this.radius < this.originalRadius * 1.3) {
                this.radius += 0.5;
            } else if (!this.hovered && this.radius > this.originalRadius) {
                this.radius -= 0.5;
            }
            this.draw();
        }
    }
    
    // Connection class
    class Connection {
        constructor(startNode, endNode) {
            this.startNode = startNode;
            this.endNode = endNode;
        }
        
        draw() {
            ctx.beginPath();
            ctx.moveTo(this.startNode.x, this.startNode.y);
            ctx.lineTo(this.endNode.x, this.endNode.y);
            ctx.strokeStyle = colors.connection;
            ctx.lineWidth = 1;
            ctx.stroke();
        }
    }
    
    // Animated Point class
    class AnimatedPoint {
        constructor(startNode, endNode) {
            this.startNode = startNode;
            this.endNode = endNode;
            this.x = startNode.x;
            this.y = startNode.y;
            this.size = 2;
            this.speed = 0.01 + Math.random() * 0.02;
            this.progress = 0;
            this.active = true;
            this.color = colors.point;
            this.opacity = 0.7;
        }
        
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
            ctx.fill();
        }
        
        update() {
            if (this.active) {
                this.progress += this.speed;
                if (this.progress >= 1) {
                    this.progress = 0;
                    this.active = Math.random() > 0.3; // 70% chance to continue
                    if (this.active) {
                        // Find a new destination node in the next layer
                        const layerIndex = layers.findIndex(layer => layer.includes(this.endNode));
                        if (layerIndex < layers.length - 1) {
                            const nextLayer = layers[layerIndex + 1];
                            this.startNode = this.endNode;
                            this.endNode = nextLayer[Math.floor(Math.random() * nextLayer.length)];
                        } else {
                            this.active = false;
                        }
                    }
                }
                
                this.x = this.startNode.x + (this.endNode.x - this.startNode.x) * this.progress;
                this.y = this.startNode.y + (this.endNode.y - this.startNode.y) * this.progress;
                this.opacity = 0.7 - Math.abs(this.progress - 0.5) * 0.4;
            }
            
            this.draw();
            
            return this.active;
        }
    }
    
    // Initialize network
    function init() {
        // Set canvas dimensions
        width = neuralNetworkCanvas.offsetWidth;
        height = neuralNetworkCanvas.offsetHeight;
        neuralNetworkCanvas.width = width;
        neuralNetworkCanvas.height = height;
        
        nodes = [];
        connections = [];
        animatedPoints = [];
        
        // Create layers
        const layerCount = 4;
        const layerSpacing = width / (layerCount + 1);
        const nodeSizes = [8, 6, 6, 7];
        const layers = [];
        
        for (let i = 0; i < layerCount; i++) {
            const nodeCount = nodeSizes[i];
            const layer = [];
            const layerX = layerSpacing * (i + 1);
            const nodeSpacing = height / (nodeCount + 1);
            
            for (let j = 0; j < nodeCount; j++) {
                const node = new Node(
                    layerX,
                    nodeSpacing * (j + 1),
                    i === 0 || i === layerCount - 1 ? 8 : 6
                );
                nodes.push(node);
                layer.push(node);
            }
            
            layers.push(layer);
        }
        
        // Create connections
        for (let i = 0; i < layerCount - 1; i++) {
            const currentLayer = layers[i];
            const nextLayer = layers[i + 1];
            
            for (const startNode of currentLayer) {
                for (const endNode of nextLayer) {
                    const connection = new Connection(startNode, endNode);
                    connections.push(connection);
                    
                    // Add animated points
                    if (Math.random() < 0.3) { // 30% chance for each connection
                        animatedPoints.push(new AnimatedPoint(startNode, endNode));
                    }
                }
            }
        }
        
        // Store layers for reference
        window.layers = layers;
    }
    
    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, width, height);
        
        // Draw connections
        for (const connection of connections) {
            connection.draw();
        }
        
        // Draw and update nodes
        for (const node of nodes) {
            node.update();
        }
        
        // Update animated points
        animatedPoints = animatedPoints.filter(point => point.update());
        
        // Occasionally add new animated points
        if (Math.random() < 0.03 && animatedPoints.length < 50) {
            const firstLayer = layers[0];
            const secondLayer = layers[1];
            const startNode = firstLayer[Math.floor(Math.random() * firstLayer.length)];
            const endNode = secondLayer[Math.floor(Math.random() * secondLayer.length)];
            animatedPoints.push(new AnimatedPoint(startNode, endNode));
        }
    }
    
    // Handle resize
    window.addEventListener('resize', () => {
        init();
    });
    
    // Initialize and start animation
    init();
    animate();
}

// Enhance interaction with expertise cards
const expertiseCards = document.querySelectorAll('.expertise-card');
if (expertiseCards.length > 0) {
    expertiseCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-15px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
}

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        if (this.getAttribute('href') !== '#') {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Zero to Hero Theme - Progress path animation
const pathSteps = document.querySelectorAll('.path-step');
if (pathSteps.length > 0) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, { threshold: 0.2 });
    
    pathSteps.forEach(step => {
        observer.observe(step);
    });
}

// Add fade-in animations to elements
function setupFadeAnimations() {
    const fadeElements = document.querySelectorAll('.section-title, .expertise-card, .project-card, .repo-card, .post-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, { threshold: 0.1 });
    
    fadeElements.forEach(element => {
        observer.observe(element);
    });
}

document.addEventListener('DOMContentLoaded', setupFadeAnimations); 