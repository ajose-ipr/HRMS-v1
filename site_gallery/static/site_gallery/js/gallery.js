/**
 * Site Gallery JavaScript utilities
 */

// Lightbox functionality
class GalleryLightbox {
    constructor() {
        this.currentPhotoIndex = 0;
        this.photos = [];
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.attachPhotoClickHandlers();
        });
    }

    attachPhotoClickHandlers() {
        const photoElements = document.querySelectorAll('.gallery-item__image');
        this.photos = Array.from(photoElements);

        photoElements.forEach((element, index) => {
            element.addEventListener('click', (e) => {
                e.preventDefault();
                this.openLightbox(index);
            });
            element.style.cursor = 'pointer';
        });
    }

    openLightbox(index) {
        this.currentPhotoIndex = index;
        const lightbox = document.getElementById('photoLightbox');
        if (!lightbox) {
            this.createLightbox();
        } else {
            lightbox.style.display = 'block';
            this.displayPhoto(index);
        }
    }

    createLightbox() {
        const lightbox = document.createElement('div');
        lightbox.id = 'photoLightbox';
        lightbox.className = 'lightbox';
        lightbox.innerHTML = `
            <div class="lightbox-content">
                <span class="lightbox-close">&times;</span>
                <div class="lightbox-container">
                    <img id="lightboxImage" src="" alt="Photo" />
                    <div id="lightboxCaption" class="lightbox-caption"></div>
                </div>
                <a class="lightbox-prev" onclick="galleryLightbox.prevPhoto()">&#10094;</a>
                <a class="lightbox-next" onclick="galleryLightbox.nextPhoto()">&#10095;</a>
            </div>
        `;

        document.body.appendChild(lightbox);

        document.querySelector('.lightbox-close').addEventListener('click', () => {
            this.closeLightbox();
        });

        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                this.closeLightbox();
            }
        });

        this.displayPhoto(0);
    }

    displayPhoto(index) {
        if (this.photos.length === 0) return;

        this.currentPhotoIndex = (index + this.photos.length) % this.photos.length;
        const img = this.photos[this.currentPhotoIndex];
        const lightboxImg = document.getElementById('lightboxImage');
        const caption = document.getElementById('lightboxCaption');

        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt;

        const item = img.closest('.gallery-item');
        if (item) {
            const captionEl = item.querySelector('.gallery-item__caption');
            caption.textContent = captionEl ? captionEl.textContent : '';
        }

        const lightbox = document.getElementById('photoLightbox');
        lightbox.style.display = 'block';
    }

    nextPhoto() {
        this.displayPhoto(this.currentPhotoIndex + 1);
    }

    prevPhoto() {
        this.displayPhoto(this.currentPhotoIndex - 1);
    }

    closeLightbox() {
        const lightbox = document.getElementById('photoLightbox');
        if (lightbox) {
            lightbox.style.display = 'none';
        }
    }
}

// Initialize gallery lightbox
let galleryLightbox = new GalleryLightbox();

// File upload utilities
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    handleFiles(files);
}

// Utility to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Debounce function for filter changes
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Format file size for display
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}
