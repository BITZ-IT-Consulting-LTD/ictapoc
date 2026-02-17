<template>
    <!-- Skip Link for Keyboard Users -->
    <a href="#main-content" class="skip-link">Skip to main content</a>

    <div class="page">
        <!-- ARIA Live Region for Announcements -->
        <div aria-live="polite" aria-atomic="true" class="sr-only" role="status">
            {{ liveMessage }}
        </div>

        <header class="page__header">
            <div class="page__title-group">
                <h1 class="page__title">Accessible Form Example</h1>
                <p class="page__subtitle">WCAG 2.1 AA/AAA Compliant Components</p>
            </div>
        </header>

        <main id="main-content" class="page__content">
            <!-- Success Message Example -->
            <div v-if="showSuccess" class="status-message status-message--success" role="status" aria-live="polite">
                <span aria-hidden="true">✓</span>
                Form submitted successfully!
            </div>

            <!-- Error Message Example -->
            <div v-if="showError" class="status-message status-message--error" role="alert">
                <span aria-hidden="true">⚠</span>
                Please correct the errors below
            </div>

            <div class="card">
                <div class="card__header">
                    <h2 class="card__title">User Registration</h2>
                </div>

                <div class="card__body">
                    <form @submit.prevent="handleSubmit" class="form">
                        <!-- Required Field with Label -->
                        <div class="form__group">
                            <label for="fullName" class="form__label form__label--required">
                                Full Name
                            </label>
                            <input id="fullName" v-model="form.fullName" type="text" class="form__input"
                                :class="{ 'form__input--error': errors.fullName }" required aria-required="true"
                                :aria-invalid="!!errors.fullName"
                                :aria-describedby="errors.fullName ? 'fullName-error' : 'fullName-helper'">
                            <span v-if="!errors.fullName" id="fullName-helper" class="form__helper-text">
                                Enter your first and last name
                            </span>
                            <div v-if="errors.fullName" id="fullName-error" class="form__error-message" role="alert">
                                {{ errors.fullName }}
                            </div>
                        </div>

                        <!-- Email Field with Validation -->
                        <div class="form__group">
                            <label for="email" class="form__label form__label--required">
                                Email Address
                            </label>
                            <input id="email" v-model="form.email" type="email" class="form__input"
                                :class="{ 'form__input--error': errors.email }" required aria-required="true"
                                :aria-invalid="!!errors.email"
                                :aria-describedby="errors.email ? 'email-error' : 'email-helper'">
                            <span v-if="!errors.email" id="email-helper" class="form__helper-text">
                                We'll never share your email with anyone
                            </span>
                            <div v-if="errors.email" id="email-error" class="form__error-message" role="alert">
                                {{ errors.email }}
                            </div>
                        </div>

                        <!-- Password Field -->
                        <div class="form__group">
                            <label for="password" class="form__label form__label--required">
                                Password
                            </label>
                            <input id="password" v-model="form.password" type="password" class="form__input"
                                :class="{ 'form__input--error': errors.password }" required aria-required="true"
                                :aria-invalid="!!errors.password"
                                :aria-describedby="errors.password ? 'password-error' : 'password-helper'"
                                minlength="8">
                            <span v-if="!errors.password" id="password-helper" class="form__helper-text">
                                Must be at least 8 characters with one number
                            </span>
                            <div v-if="errors.password" id="password-error" class="form__error-message" role="alert">
                                {{ errors.password }}
                            </div>
                        </div>

                        <!-- Select Field -->
                        <div class="form__group">
                            <label for="role" class="form__label form__label--required">
                                User Role
                            </label>
                            <select id="role" v-model="form.role" class="form__select"
                                :class="{ 'form__select--error': errors.role }" required aria-required="true"
                                :aria-invalid="!!errors.role"
                                :aria-describedby="errors.role ? 'role-error' : undefined">
                                <option value="">Select a role...</option>
                                <option value="citizen">Citizen</option>
                                <option value="staff">Staff Member</option>
                                <option value="admin">Administrator</option>
                            </select>
                            <div v-if="errors.role" id="role-error" class="form__error-message" role="alert">
                                {{ errors.role }}
                            </div>
                        </div>

                        <!-- Textarea Field -->
                        <div class="form__group">
                            <label for="bio" class="form__label">
                                Bio (Optional)
                            </label>
                            <textarea id="bio" v-model="form.bio" class="form__textarea"
                                :aria-describedby="'bio-helper'" rows="4"></textarea>
                            <span id="bio-helper" class="form__helper-text">
                                Tell us a bit about yourself (max 500 characters)
                            </span>
                        </div>

                        <!-- Form Actions -->
                        <div class="flex gap-2 justify-between items-center">
                            <button type="button" @click="resetForm" class="button button--secondary"
                                :disabled="isSubmitting">
                                Reset Form
                            </button>

                            <button type="submit" class="button button--primary"
                                :class="{ 'button--loading': isSubmitting }" :disabled="isSubmitting"
                                :aria-busy="isSubmitting">
                                <span v-if="!isSubmitting">Submit Application</span>
                                <span v-else class="sr-only">Submitting...</span>
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Additional Examples Section -->
            <div class="card">
                <div class="card__header">
                    <h2 class="card__title">Accessible Components Gallery</h2>
                </div>

                <div class="card__body">
                    <!-- Status Messages -->
                    <section class="mb-4">
                        <h3 class="text-main font-bold mb-2">Status Messages</h3>
                        <div class="status-message status-message--success" role="status">
                            <span aria-hidden="true">✓</span>
                            Success message with icon
                        </div>
                        <div class="status-message status-message--error" role="alert">
                            <span aria-hidden="true">⚠</span>
                            Error message with icon
                        </div>
                        <div class="status-message status-message--warning" role="status">
                            <span aria-hidden="true">⚠</span>
                            Warning message with icon
                        </div>
                        <div class="status-message status-message--info" role="status">
                            <span aria-hidden="true">ℹ</span>
                            Info message with icon
                        </div>
                    </section>

                    <!-- Badges -->
                    <section class="mb-4">
                        <h3 class="text-main font-bold mb-2">Status Badges</h3>
                        <div class="flex gap-2 items-center">
                            <span class="badge badge--success" role="status">Active</span>
                            <span class="badge badge--danger" role="status">Rejected</span>
                            <span class="badge badge--warning" role="status">Pending</span>
                            <span class="badge badge--info" role="status">In Review</span>
                        </div>
                    </section>

                    <!-- Buttons -->
                    <section class="mb-4">
                        <h3 class="text-main font-bold mb-2">Button Variants</h3>
                        <div class="flex gap-2 items-center flex-wrap">
                            <button class="button button--primary">Primary Button</button>
                            <button class="button button--secondary">Secondary Button</button>
                            <button class="button button--ghost">Ghost Button</button>
                            <button class="button button--primary button--small">Small Button</button>
                            <button class="button button--icon" aria-label="Settings" title="Settings">
                                <span aria-hidden="true">⚙</span>
                                <span class="sr-only">Settings</span>
                            </button>
                            <button class="button button--primary" disabled>Disabled Button</button>
                        </div>
                    </section>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
    import { ref, reactive } from 'vue';

    const liveMessage = ref('');
    const showSuccess = ref(false);
    const showError = ref(false);
    const isSubmitting = ref(false);

    const form = reactive({
        fullName: '',
        email: '',
        password: '',
        role: '',
        bio: ''
    });

    const errors = reactive({
        fullName: '',
        email: '',
        password: '',
        role: ''
    });

    const validateForm = () => {
        let isValid = true;

        // Reset errors
        Object.keys(errors).forEach(key => errors[key] = '');

        // Validate full name
        if (!form.fullName.trim()) {
            errors.fullName = 'Full name is required';
            isValid = false;
        } else if (form.fullName.trim().length < 3) {
            errors.fullName = 'Full name must be at least 3 characters';
            isValid = false;
        }

        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!form.email.trim()) {
            errors.email = 'Email address is required';
            isValid = false;
        } else if (!emailRegex.test(form.email)) {
            errors.email = 'Please enter a valid email address';
            isValid = false;
        }

        // Validate password
        if (!form.password) {
            errors.password = 'Password is required';
            isValid = false;
        } else if (form.password.length < 8) {
            errors.password = 'Password must be at least 8 characters';
            isValid = false;
        } else if (!/\d/.test(form.password)) {
            errors.password = 'Password must contain at least one number';
            isValid = false;
        }

        // Validate role
        if (!form.role) {
            errors.role = 'Please select a user role';
            isValid = false;
        }

        return isValid;
    };

    const handleSubmit = async () => {
        showSuccess.value = false;
        showError.value = false;

        if (!validateForm()) {
            showError.value = true;
            liveMessage.value = 'Form contains errors. Please review and correct them.';

            // Focus first error field
            setTimeout(() => {
                const firstError = Object.keys(errors).find(key => errors[key]);
                if (firstError) {
                    document.getElementById(firstError)?.focus();
                }
            }, 100);

            return;
        }

        isSubmitting.value = true;
        liveMessage.value = 'Submitting form...';

        // Simulate API call
        setTimeout(() => {
            isSubmitting.value = false;
            showSuccess.value = true;
            showError.value = false;
            liveMessage.value = 'Form submitted successfully!';

            console.log('Form submitted:', form);
        }, 2000);
    };

    const resetForm = () => {
        Object.keys(form).forEach(key => form[key] = '');
        Object.keys(errors).forEach(key => errors[key] = '');
        showSuccess.value = false;
        showError.value = false;
        liveMessage.value = 'Form has been reset';
    };
</script>

<style scoped>

    /* Additional component-specific styles if needed */
    .font-bold {
        font-weight: 700;
    }

    .text-main {
        color: var(--text-main);
    }

    .flex-wrap {
        flex-wrap: wrap;
    }
</style>
