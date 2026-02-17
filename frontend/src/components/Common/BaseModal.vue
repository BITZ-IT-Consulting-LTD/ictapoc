<template>
    <Teleport to="body">
        <Transition name="modal-fade">
            <div v-if="show" class="modal" role="dialog" aria-modal="true" @mousedown.self="onBackdropClick">
                <div class="modal__overlay"></div>
                <div ref="modalCard" class="modal__card" :class="[`modal__card--${size}`]" tabindex="-1"
                    @keydown.esc="close">
                    <!-- Header -->
                    <header v-if="$slots.header || title" class="modal__header" :class="headerClass">
                        <slot name="header">
                            <div class="modal__header-content">
                                <h3 class="modal__title">{{ title }}</h3>
                                <p v-if="subtitle" class="modal__subtitle">{{ subtitle }}</p>
                            </div>
                        </slot>
                        <button class="modal__close" @click="close" aria-label="Close modal">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </header>

                    <!-- Body -->
                    <main class="modal__body">
                        <!-- Error Alert Section -->
                        <div v-if="error" class="alert alert--danger animate-fade-in">
                            <i class="bi bi-exclamation-triangle-fill"></i>
                            <span>{{ error }}</span>
                        </div>

                        <!-- Loading Overlay -->
                        <div v-if="loading" class="modal__loading">
                            <div class="spinner"></div>
                            <p>Processing...</p>
                        </div>

                        <slot></slot>
                    </main>

                    <!-- Footer -->
                    <footer v-if="$slots.footer" class="modal__footer" :class="footerClass">
                        <slot name="footer"></slot>
                    </footer>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup>
    import { ref, watch, onMounted, onUnmounted } from 'vue';

    const props = defineProps({
        show: Boolean,
        title: String,
        subtitle: String,
        icon: String,
        error: String,
        loading: Boolean,
        size: {
            type: String,
            default: 'md',
            validator: (v) => ['sm', 'md', 'lg', 'full'].includes(v)
        },
        closeOnBackdrop: {
            type: Boolean,
            default: true
        },
        closeOnEsc: {
            type: Boolean,
            default: true
        },
        headerClass: String,
        footerClass: String
    });

    const emit = defineEmits(['update:show', 'close']);
    const modalCard = ref(null);

    const close = () => {
        emit('update:show', false);
        emit('close');
    };

    const onBackdropClick = () => {
        if (props.closeOnBackdrop) close();
    };

    const handleEsc = (e) => {
        if (props.show && props.closeOnEsc && e.key === 'Escape') {
            close();
        }
    };

    // Trap focus logic
    const focusTrap = (e) => {
        if (!modalCard.value) return;
        const focusableElements = modalCard.value.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusableElements.length === 0) return;

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    lastElement.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastElement) {
                    firstElement.focus();
                    e.preventDefault();
                }
            }
        }
    };

    watch(() => props.show, (newVal) => {
        if (newVal) {
            document.body.style.overflow = 'hidden';
            document.body.style.paddingRight = 'var(--scrollbar-width, 0px)';

            // Focus management
            setTimeout(() => {
                if (modalCard.value) {
                    const focusable = modalCard.value.querySelector('button, input, select, textarea');
                    if (focusable) focusable.focus();
                    else modalCard.value.focus();
                }
            }, 100);

            window.addEventListener('keydown', focusTrap);
        } else {
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
            window.removeEventListener('keydown', focusTrap);
        }
    });

    onMounted(() => {
        window.addEventListener('keydown', handleEsc);

        // Calculate scrollbar width to prevent layout shift
        const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
        document.documentElement.style.setProperty('--scrollbar-width', `${scrollbarWidth}px`);
    });

    onUnmounted(() => {
        window.removeEventListener('keydown', handleEsc);
        window.removeEventListener('keydown', focusTrap);
        document.body.style.overflow = '';
    });
</script>

<style scoped>
    .modal-error-alert {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        color: #e11d48;
        padding: 1rem;
        border-radius: var(--radius-md);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.875rem;
        font-weight: 600;
    }

    .modal-loading-overlay {
        position: absolute;
        inset: 0;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(2px);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10;
        border-radius: var(--radius-lg);
    }

    .spinner {
        width: 2.5rem;
        height: 2.5rem;
        border: 3px solid #f1f5f9;
        border-top-color: var(--icta-red);
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-bottom: 1rem;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .animate-fade-in {
        animation: fadeIn 0.3s ease;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
