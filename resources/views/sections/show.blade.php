<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight animate-fade-in">{{ $section->title }}</h2>
            <div class="flex items-center space-x-3">
                @if(session('study_flow'))
                <a href="{{ route('study-flow.exit') }}" class="inline-flex items-center px-4 py-2 bg-gray-500 text-white rounded-lg font-semibold text-xs uppercase tracking-widest hover:bg-gray-600 transition-all duration-200">
                    Exit Flow
                </a>
                @endif
                <a href="{{ route('sections.index') }}" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 transition-colors duration-200">
                    <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                    Back to Sections
                </a>
            </div>
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            @if(session('success'))
            <div class="mb-6 bg-gradient-to-r from-green-400 to-emerald-500 text-white px-6 py-4 rounded-xl shadow-lg animate-fade-in-down flex items-center">
                <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ session('success') }}
            </div>
            @endif

            <!-- Section Info Card -->
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl rounded-2xl mb-8 animate-fade-in-up">
                <div class="p-8">
                    <div class="flex items-center mb-6">
                        <div class="w-16 h-16 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center text-white text-3xl shadow-lg">
                            📑
                        </div>
                        <div class="ml-6">
                            <h3 class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ $section->title }}</h3>
                            <p class="text-gray-500 dark:text-gray-400">{{ $section->lecture->title ?? 'N/A' }} • {{ $section->lecture->subject->name ?? 'N/A' }}</p>
                        </div>
                    </div>

                    <!-- Quick Summary -->
                    @if($section->quick_summary)
                    <div class="mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-xl">
                        <p class="text-gray-600 dark:text-gray-400">{{ $section->quick_summary }}</p>
                    </div>
                    @endif

                    <!-- Links -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        @if($section->notebook_link)
                        <a href="{{ $section->notebook_link }}" target="_blank" class="flex items-center p-4 bg-gradient-to-r from-blue-50 to-indigo-100 dark:from-gray-700 dark:to-gray-600 rounded-xl hover:shadow-lg transition-all duration-200">
                            <div class="w-12 h-12 rounded-lg bg-blue-500 flex items-center justify-center text-white mr-4">📓</div>
                            <div>
                                <p class="font-semibold text-gray-900 dark:text-gray-100">Google NotebookLM</p>
                                <p class="text-sm text-gray-500 dark:text-gray-400">Open in new tab</p>
                            </div>
                        </a>
                        @endif
                        @if($section->dynamic_view_link)
                        <a href="{{ $section->dynamic_view_link }}" target="_blank" class="flex items-center p-4 bg-gradient-to-r from-green-50 to-emerald-100 dark:from-gray-700 dark:to-gray-600 rounded-xl hover:shadow-lg transition-all duration-200">
                            <div class="w-12 h-12 rounded-lg bg-green-500 flex items-center justify-center text-white mr-4">🔗</div>
                            <div>
                                <p class="font-semibold text-gray-900 dark:text-gray-100">Google Dynamic View</p>
                                <p class="text-sm text-gray-500 dark:text-gray-400">Open in new tab</p>
                            </div>
                        </a>
                        @endif
                    </div>
                </div>
            </div>

            <!-- Study Flow: Content Management Panel -->
            @if(session('study_flow') && Auth::check() && Auth::user()->role === 'admin')
            <div class="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl shadow-xl p-6 mb-8 animate-fade-in-up" style="animation-delay: 0.1s">
                <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-6">🎯 Add Content to this Section</h4>

                <form action="{{ route('study-flow.bulk-content', $section) }}" method="POST">
                    @csrf

                    <!-- Links Section -->
                    <div class="bg-white dark:bg-gray-800 rounded-xl p-4 mb-4 border border-gray-200 dark:border-gray-600">
                        <h5 class="font-semibold text-gray-700 dark:text-gray-300 mb-4 flex items-center">
                            <span class="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mr-3">🔗</span>
                            Update Links
                        </h5>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Google NotebookLM Link</label>
                                <input type="url" name="notebook_link" value="{{ $section->notebook_link }}" placeholder="https://" class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Google Dynamic View Link</label>
                                <input type="url" name="dynamic_view_link" value="{{ $section->dynamic_view_link }}" placeholder="https://" class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white">
                            </div>
                        </div>
                    </div>

                    <!-- Questions Section -->
                    <div class="bg-white dark:bg-gray-800 rounded-xl p-4 mb-4 border border-gray-200 dark:border-gray-600">
                        <div class="flex items-center justify-between mb-4">
                            <h5 class="font-semibold text-gray-700 dark:text-gray-300 flex items-center">
                                <span class="w-8 h-8 bg-green-100 text-green-600 rounded-full flex items-center justify-center mr-3">❓</span>
                                Add Questions
                            </h5>
                            <div class="flex items-center space-x-2">
                                <input type="number" id="question-count" min="0" max="10" value="0" class="w-16 rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white text-sm">
                                <button type="button" onclick="generateQuestionForms()" class="px-3 py-1 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition-colors">Generate</button>
                            </div>
                        </div>
                        <div id="question-forms-container" class="space-y-3"></div>
                    </div>

                    <!-- Exam Questions Section -->
                    <div class="bg-white dark:bg-gray-800 rounded-xl p-4 mb-4 border border-gray-200 dark:border-gray-600">
                        <div class="flex items-center justify-between mb-4">
                            <h5 class="font-semibold text-gray-700 dark:text-gray-300 flex items-center">
                                <span class="w-8 h-8 bg-red-100 text-red-600 rounded-full flex items-center justify-center mr-3">📝</span>
                                Add Exam Questions
                            </h5>
                            <div class="flex items-center space-x-2">
                                <input type="number" id="exam-question-count" min="0" max="10" value="0" class="w-16 rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white text-sm">
                                <button type="button" onclick="generateExamQuestionForms()" class="px-3 py-1 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition-colors">Generate</button>
                            </div>
                        </div>
                        <div id="exam-question-forms-container" class="space-y-3"></div>
                    </div>

                    <div class="flex justify-end">
                        <button type="submit" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-xl font-bold hover:from-green-600 hover:to-emerald-600 transition-all duration-300 transform hover:scale-105 shadow-lg">
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                            </svg>
                            Save All Content
                        </button>
                    </div>
                </form>
            </div>
            @endif

            @if(Auth::check() && Auth::user()->role !== 'student')
            <div class="flex space-x-4 animate-fade-in-up" style="animation-delay: 0.3s">
                <a href="{{ route('sections.edit', $section) }}" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-semibold hover:from-amber-600 hover:to-orange-600 transition-all duration-300 transform hover:scale-105 shadow-lg">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Edit Section
                </a>
                <form action="{{ route('sections.destroy', $section) }}" method="POST" class="inline">
                    @csrf
                    @method('DELETE')
                    <button type="submit" onclick="return confirm('Are you sure?')" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-red-500 to-rose-500 text-white rounded-xl font-semibold hover:from-red-600 hover:to-rose-600 transition-all duration-300 transform hover:scale-105 shadow-lg">
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Delete
                    </button>
                </form>
            </div>
            @endif
        </div>
    </div>

    <style>
        @keyframes fadeIn {
            from {
                opacity: 0;
            }

            to {
                opacity: 1;
            }
        }

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

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .animate-fade-in {
            animation: fadeIn 0.5s ease-out forwards;
        }

        .animate-fade-in-up {
            animation: fadeInUp 0.5s ease-out forwards;
            opacity: 0;
        }

        .animate-fade-in-down {
            animation: fadeInDown 0.5s ease-out forwards;
        }
    </style>

    <script>
        function generateQuestionForms() {
            const count = parseInt(document.getElementById('question-count').value) || 0;
            const container = document.getElementById('question-forms-container');
            container.innerHTML = '';
            for (let i = 0; i < count; i++) {
                container.innerHTML += `
                    <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Idea *</label>
                                <textarea name="questions[${i}][idea]" required rows="2" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white"></textarea>
                            </div>
                            <div>
                                <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Explanation</label>
                                <textarea name="questions[${i}][explanation]" rows="2" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white"></textarea>
                            </div>
                        </div>
                    </div>
                `;
            }
        }

        function generateExamQuestionForms() {
            const count = parseInt(document.getElementById('exam-question-count').value) || 0;
            const container = document.getElementById('exam-question-forms-container');
            container.innerHTML = '';
            for (let i = 0; i < count; i++) {
                container.innerHTML += `
                    <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Idea *</label>
                                <textarea name="exam_questions[${i}][idea]" required rows="2" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white"></textarea>
                            </div>
                            <div>
                                <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Explanation</label>
                                <textarea name="exam_questions[${i}][explanation]" rows="2" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white"></textarea>
                            </div>
                        </div>
                    </div>
                `;
            }
        }
    </script>
</x-app-layout>