<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ config('app.name', 'EduPlatform') }} - Learn, Grow, Succeed</title>
    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=inter:400,500,600,700,800&display=swap" rel="stylesheet" />
    @vite(['resources/css/app.css', 'resources/js/app.js'])
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInLeft {
            from {
                opacity: 0;
                transform: translateX(-40px);
            }

            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes fadeInRight {
            from {
                opacity: 0;
                transform: translateX(40px);
            }

            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes float {

            0%,
            100% {
                transform: translateY(0px);
            }

            50% {
                transform: translateY(-20px);
            }
        }

        @keyframes pulse {

            0%,
            100% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.05);
            }
        }

        @keyframes gradient {
            0% {
                background-position: 0% 50%;
            }

            50% {
                background-position: 100% 50%;
            }

            100% {
                background-position: 0% 50%;
            }
        }

        .animate-fade-in-up {
            animation: fadeInUp 0.8s ease-out forwards;
            opacity: 0;
        }

        .animate-fade-in-left {
            animation: fadeInLeft 0.8s ease-out forwards;
            opacity: 0;
        }

        .animate-fade-in-right {
            animation: fadeInRight 0.8s ease-out forwards;
            opacity: 0;
        }

        .animate-float {
            animation: float 3s ease-in-out infinite;
        }

        .animate-pulse-slow {
            animation: pulse 2s ease-in-out infinite;
        }

        .gradient-animate {
            background: linear-gradient(-45deg, #667eea, #764ba2, #6B8DD6, #8E37D7);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }

        .hover-lift {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .hover-lift:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>

<body class="antialiased bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-b border-gray-200 dark:border-gray-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-2">
                    <span class="text-2xl">📚</span>
                    <span class="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">EduPlatform</span>
                </div>
                <div class="flex items-center space-x-4">
                    @auth
                    <a href="{{ route('dashboard') }}" class="text-gray-700 dark:text-gray-300 hover:text-indigo-600 font-medium transition-colors">Dashboard</a>
                    @else
                    <a href="{{ route('login') }}" class="text-gray-700 dark:text-gray-300 hover:text-indigo-600 font-medium transition-colors">Login</a>
                    @if (Route::has('register'))
                    <a href="{{ route('register') }}" class="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg transition-all">Register</a>
                    @endif
                    @endauth
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="min-h-screen flex items-center gradient-animate pt-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div class="animate-fade-in-left">
                    <span class="inline-block px-4 py-2 bg-white/20 backdrop-blur-sm text-white rounded-full text-sm font-medium mb-6">🎓 Welcome to the Future of Learning</span>
                    <h1 class="text-5xl lg:text-6xl font-extrabold text-white leading-tight mb-6">
                        Learn Without<br>
                        <span class="bg-gradient-to-r from-yellow-300 to-orange-400 bg-clip-text text-transparent">Limits</span>
                    </h1>
                    <p class="text-xl text-white/80 mb-8 max-w-lg">
                        Access world-class lectures, practice questions, and exam preparation materials. Your journey to success starts here.
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4">
                        @auth
                        <a href="{{ route('dashboard') }}" class="inline-flex items-center justify-center px-8 py-4 bg-white text-indigo-600 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-all hover-lift">
                            Go to Dashboard
                            <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                            </svg>
                        </a>
                        @else
                        <a href="{{ route('register') }}" class="inline-flex items-center justify-center px-8 py-4 bg-white text-indigo-600 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-all hover-lift">
                            Get Started Free
                            <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                            </svg>
                        </a>
                        <a href="{{ route('login') }}" class="inline-flex items-center justify-center px-8 py-4 bg-white/10 backdrop-blur-sm text-white border border-white/30 rounded-xl font-semibold text-lg hover:bg-white/20 transition-all">
                            Sign In
                        </a>
                        @endauth
                    </div>
                </div>
                <div class="animate-fade-in-right hidden lg:block">
                    <div class="relative">
                        <div class="absolute -inset-4 bg-white/10 rounded-3xl backdrop-blur-sm"></div>
                        <div class="relative bg-white/20 rounded-2xl p-8 backdrop-blur-sm animate-float">
                            <div class="grid grid-cols-2 gap-4">
                                <div class="bg-white/30 rounded-xl p-6 text-center">
                                    <span class="text-4xl">📖</span>
                                    <p class="text-white font-semibold mt-2">50+ Lectures</p>
                                </div>
                                <div class="bg-white/30 rounded-xl p-6 text-center">
                                    <span class="text-4xl">❓</span>
                                    <p class="text-white font-semibold mt-2">200+ Questions</p>
                                </div>
                                <div class="bg-white/30 rounded-xl p-6 text-center">
                                    <span class="text-4xl">🎯</span>
                                    <p class="text-white font-semibold mt-2">100+ Exam Qs</p>
                                </div>
                                <div class="bg-white/30 rounded-xl p-6 text-center">
                                    <span class="text-4xl">👩‍🎓</span>
                                    <p class="text-white font-semibold mt-2">500+ Students</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="py-24 bg-white dark:bg-gray-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16 animate-fade-in-up" style="animation-delay: 0.2s;">
                <span class="inline-block px-4 py-2 bg-indigo-100 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-400 rounded-full text-sm font-medium mb-4">Features</span>
                <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">Everything You Need to Succeed</h2>
                <p class="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">Our platform provides comprehensive tools for students, teachers, and administrators.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div class="bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-700 dark:to-gray-600 rounded-2xl p-8 hover-lift animate-fade-in-up" style="animation-delay: 0.3s;">
                    <div class="w-14 h-14 bg-blue-500 rounded-xl flex items-center justify-center mb-6">
                        <span class="text-2xl">📚</span>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Rich Lectures</h3>
                    <p class="text-gray-600 dark:text-gray-300">Access comprehensive lectures with PDF materials, summaries, and organized sections.</p>
                </div>

                <div class="bg-gradient-to-br from-green-50 to-emerald-100 dark:from-gray-700 dark:to-gray-600 rounded-2xl p-8 hover-lift animate-fade-in-up" style="animation-delay: 0.4s;">
                    <div class="w-14 h-14 bg-green-500 rounded-xl flex items-center justify-center mb-6">
                        <span class="text-2xl">❓</span>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Practice Questions</h3>
                    <p class="text-gray-600 dark:text-gray-300">Sharpen your skills with practice questions featuring hints and detailed solutions.</p>
                </div>

                <div class="bg-gradient-to-br from-purple-50 to-violet-100 dark:from-gray-700 dark:to-gray-600 rounded-2xl p-8 hover-lift animate-fade-in-up" style="animation-delay: 0.5s;">
                    <div class="w-14 h-14 bg-purple-500 rounded-xl flex items-center justify-center mb-6">
                        <span class="text-2xl">📝</span>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Exam Preparation</h3>
                    <p class="text-gray-600 dark:text-gray-300">Prepare for exams with real exam-style questions and comprehensive explanations.</p>
                </div>

                <div class="bg-gradient-to-br from-yellow-50 to-amber-100 dark:from-gray-700 dark:to-gray-600 rounded-2xl p-8 hover-lift animate-fade-in-up" style="animation-delay: 0.6s;">
                    <div class="w-14 h-14 bg-yellow-500 rounded-xl flex items-center justify-center mb-6">
                        <span class="text-2xl">❤️</span>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Favorites System</h3>
                    <p class="text-gray-600 dark:text-gray-300">Save your favorite lectures and questions for quick access anytime.</p>
                </div>

                <div class="bg-gradient-to-br from-red-50 to-rose-100 dark:from-gray-700 dark:to-gray-600 rounded-2xl p-8 hover-lift animate-fade-in-up" style="animation-delay: 0.7s;">
                    <div class="w-14 h-14 bg-red-500 rounded-xl flex items-center justify-center mb-6">
                        <span class="text-2xl">👨‍🏫</span>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Expert Teachers</h3>
                    <p class="text-gray-600 dark:text-gray-300">Learn from qualified teachers with specific subject expertise and permissions.</p>
                </div>

                <div class="bg-gradient-to-br from-cyan-50 to-teal-100 dark:from-gray-700 dark:to-gray-600 rounded-2xl p-8 hover-lift animate-fade-in-up" style="animation-delay: 0.8s;">
                    <div class="w-14 h-14 bg-cyan-500 rounded-xl flex items-center justify-center mb-6">
                        <span class="text-2xl">📊</span>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Personal Dashboard</h3>
                    <p class="text-gray-600 dark:text-gray-300">Track your progress with personalized dashboards based on your role.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="py-24 gradient-animate">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div class="animate-fade-in-up">
                <h2 class="text-4xl font-bold text-white mb-6">Ready to Start Learning?</h2>
                <p class="text-xl text-white/80 mb-8">Join thousands of students already learning on our platform.</p>
                @guest
                <a href="{{ route('register') }}" class="inline-flex items-center justify-center px-10 py-4 bg-white text-indigo-600 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-all hover-lift animate-pulse-slow">
                    Create Free Account
                    <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                    </svg>
                </a>
                @else
                <a href="{{ route('dashboard') }}" class="inline-flex items-center justify-center px-10 py-4 bg-white text-indigo-600 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-all hover-lift">
                    Go to Dashboard
                    <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                    </svg>
                </a>
                @endguest
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="flex items-center space-x-2 mb-4 md:mb-0">
                    <span class="text-2xl">📚</span>
                    <span class="text-xl font-bold text-white">EduPlatform</span>
                </div>
                <p class="text-gray-400 text-sm">© {{ date('Y') }} EduPlatform. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Intersection Observer for scroll animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                }
            });
        }, {
            threshold: 0.1
        });

        document.querySelectorAll('.animate-fade-in-up, .animate-fade-in-left, .animate-fade-in-right').forEach(el => {
            el.style.animationPlayState = 'paused';
            observer.observe(el);
        });
    </script>
</body>

</html>