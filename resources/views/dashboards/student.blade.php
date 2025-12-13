<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">
            {{ __('Student Dashboard') }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <!-- Welcome Banner -->
            <div class="bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl shadow-lg p-6 mb-8 text-white animate-fade-in-up">
                <h3 class="text-2xl font-bold">Welcome, {{ auth()->user()->name }}! 📚</h3>
                <p class="mt-2 text-green-100">Start learning by exploring subjects and lectures below.</p>
            </div>

            <!-- Subjects Grid -->
            <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.2s;">
                <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">📖 Available Subjects</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    @foreach($subjects as $index => $subject)
                    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 animate-fade-in-up" style="animation-delay: {{ 0.3 + ($index * 0.1) }}s;">
                        <div class="flex items-center justify-between mb-3">
                            <h4 class="text-lg font-medium text-gray-900 dark:text-gray-100">{{ $subject->name }}</h4>
                            <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">{{ $subject->lectures_count }} lectures</span>
                        </div>
                        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">{{ Str::limit($subject->description, 80) }}</p>
                        <a href="{{ route('subjects.show', $subject) }}" class="inline-flex items-center text-blue-600 hover:text-blue-800 text-sm font-medium">
                            Explore Subject
                            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                            </svg>
                        </a>
                    </div>
                    @endforeach
                </div>
            </div>

            <!-- Recent Lectures -->
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden mb-8 animate-fade-in-up" style="animation-delay: 0.6s;">
                <div class="px-6 py-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-700 dark:to-gray-800 border-b dark:border-gray-700">
                    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">🎬 Recent Lectures</h3>
                </div>
                <div class="p-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        @foreach($recentLectures as $index => $lecture)
                        <div class="border dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-300 animate-fade-in-up" style="animation-delay: {{ 0.7 + ($index * 0.05) }}s;">
                            <div class="flex items-start justify-between">
                                <div>
                                    <h4 class="font-medium text-gray-900 dark:text-gray-100">{{ $lecture->title }}</h4>
                                    <p class="text-sm text-gray-500 dark:text-gray-400">{{ $lecture->subject->name ?? 'N/A' }}</p>
                                </div>
                                <button onclick="toggleLove('lecture', {{ $lecture->id }}, this)" class="love-btn p-2 rounded-full hover:bg-red-50 transition-colors duration-200 {{ auth()->user()->loves($lecture) ? 'text-red-500' : 'text-gray-400' }}">
                                    <svg class="w-6 h-6" fill="{{ auth()->user()->loves($lecture) ? 'currentColor' : 'none' }}" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                                    </svg>
                                </button>
                            </div>
                            <a href="{{ route('lectures.show', $lecture) }}" class="mt-3 inline-block text-blue-600 hover:text-blue-800 text-sm">View Lecture →</a>
                        </div>
                        @endforeach
                    </div>
                </div>
            </div>

            <!-- Loved Items -->
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden animate-fade-in-up" style="animation-delay: 0.9s;">
                <div class="px-6 py-4 bg-gradient-to-r from-pink-50 to-red-50 dark:from-gray-700 dark:to-gray-800 border-b dark:border-gray-700">
                    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">❤️ My Favorites</h3>
                </div>
                <div class="p-6">
                    @if($lovedLectures->count() + $lovedQuestions->count() + $lovedExamQuestions->count() > 0)
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <!-- Loved Lectures -->
                        <div>
                            <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3 flex items-center">
                                <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                                Lectures ({{ $lovedLectures->count() }})
                            </h4>
                            @foreach($lovedLectures as $lecture)
                            <a href="{{ route('lectures.show', $lecture) }}" class="block mb-2 p-3 bg-blue-50 dark:bg-gray-700 rounded-lg hover:bg-blue-100 dark:hover:bg-gray-600 transition-colors duration-200">
                                <span class="text-sm text-gray-900 dark:text-gray-100">{{ Str::limit($lecture->title, 30) }}</span>
                            </a>
                            @endforeach
                        </div>

                        <!-- Loved Questions -->
                        <div>
                            <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3 flex items-center">
                                <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                                Questions ({{ $lovedQuestions->count() }})
                            </h4>
                            @foreach($lovedQuestions as $question)
                            <a href="{{ route('questions.show', $question) }}" class="block mb-2 p-3 bg-green-50 dark:bg-gray-700 rounded-lg hover:bg-green-100 dark:hover:bg-gray-600 transition-colors duration-200">
                                <span class="text-sm text-gray-900 dark:text-gray-100">{{ Str::limit($question->idea_text, 30) }}</span>
                            </a>
                            @endforeach
                        </div>

                        <!-- Loved Exam Questions -->
                        <div>
                            <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3 flex items-center">
                                <span class="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                                Exam Questions ({{ $lovedExamQuestions->count() }})
                            </h4>
                            @foreach($lovedExamQuestions as $examQuestion)
                            <a href="{{ route('exam_questions.show', $examQuestion) }}" class="block mb-2 p-3 bg-purple-50 dark:bg-gray-700 rounded-lg hover:bg-purple-100 dark:hover:bg-gray-600 transition-colors duration-200">
                                <span class="text-sm text-gray-900 dark:text-gray-100">{{ Str::limit($examQuestion->idea, 30) }}</span>
                            </a>
                            @endforeach
                        </div>
                    </div>
                    @else
                    <div class="text-center py-8">
                        <span class="text-6xl mb-4 block">💝</span>
                        <p class="text-gray-500 dark:text-gray-400">You haven't added any favorites yet.</p>
                        <p class="text-sm text-gray-400 mt-2">Click the heart icon on lectures and questions to save them here!</p>
                    </div>
                    @endif
                </div>
            </div>
        </div>
    </div>

    <style>
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .animate-fade-in-up {
            animation: fadeInUp 0.6s ease-out forwards;
            opacity: 0;
        }

        @keyframes heartBeat {

            0%,
            100% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.2);
            }
        }

        .love-btn.loved svg {
            animation: heartBeat 0.3s ease-in-out;
        }
    </style>

    <script>
        function toggleLove(type, id, button) {
            fetch('{{ route("love.toggle") }}', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': '{{ csrf_token() }}'
                    },
                    body: JSON.stringify({
                        type: type,
                        id: id
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const svg = button.querySelector('svg');
                        if (data.is_loved) {
                            button.classList.remove('text-gray-400');
                            button.classList.add('text-red-500', 'loved');
                            svg.setAttribute('fill', 'currentColor');
                        } else {
                            button.classList.remove('text-red-500', 'loved');
                            button.classList.add('text-gray-400');
                            svg.setAttribute('fill', 'none');
                        }
                    }
                });
        }
    </script>
</x-app-layout>