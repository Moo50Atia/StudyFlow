<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">{{ $lecture->title }}</h2>
            <div class="flex items-center space-x-4">
                @auth
                <button onclick="toggleLove('lecture', {{ $lecture->id }}, this)" class="love-btn inline-flex items-center px-3 py-2 border rounded-md transition-all duration-200 {{ auth()->user()->loves($lecture) ? 'border-red-300 text-red-500 bg-red-50' : 'border-gray-300 text-gray-400 hover:bg-gray-50' }}">
                    <svg class="w-5 h-5 mr-1" fill="{{ auth()->user()->loves($lecture) ? 'currentColor' : 'none' }}" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                    <span class="text-sm">{{ auth()->user()->loves($lecture) ? 'Loved' : 'Love' }}</span>
                </button>
                @endauth
                <a href="{{ route('lectures.index') }}" class="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400">← Back</a>
            </div>
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg animate-fade-in-up">
                <div class="p-6 text-gray-900 dark:text-gray-100">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div class="animate-fade-in-up" style="animation-delay: 0.1s;">
                            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Subject</h3>
                            <p class="mt-1 text-gray-900 dark:text-gray-100">{{ $lecture->subject->name ?? 'N/A' }}</p>
                        </div>
                        <div class="animate-fade-in-up" style="animation-delay: 0.2s;">
                            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">PDF Document</h3>
                            @if($lecture->pdf_path)
                            <a href="{{ Storage::url($lecture->pdf_path) }}" target="_blank" class="mt-1 inline-flex items-center text-indigo-600 hover:text-indigo-900">
                                <svg class="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"></path>
                                </svg>
                                Download PDF
                            </a>
                            @else
                            <span class="text-gray-400">No PDF uploaded</span>
                            @endif
                        </div>
                    </div>

                    <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.3s;">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Summary</h3>
                        <p class="mt-1 text-gray-600 dark:text-gray-400">{{ $lecture->summary ?? 'No summary available.' }}</p>
                    </div>

                    <!-- Sections -->
                    <div class="border-t dark:border-gray-700 pt-6 mb-6 animate-fade-in-up" style="animation-delay: 0.4s;">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">📚 Sections ({{ $lecture->sections->count() }})</h3>
                        @if($lecture->sections->count() > 0)
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            @foreach($lecture->sections as $section)
                            <a href="{{ route('sections.show', $section) }}" class="block p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors duration-200">
                                <h4 class="font-medium text-gray-900 dark:text-gray-100">{{ $section->title }}</h4>
                                <p class="text-sm text-gray-500 dark:text-gray-400">{{ Str::limit($section->quick_summary, 60) }}</p>
                            </a>
                            @endforeach
                        </div>
                        @else
                        <p class="text-gray-500 dark:text-gray-400">No sections available.</p>
                        @endif
                    </div>

                    <!-- Questions & Exam Questions Stats -->
                    <div class="grid grid-cols-2 gap-4 animate-fade-in-up" style="animation-delay: 0.5s;">
                        <div class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 text-center">
                            <span class="text-2xl font-bold text-blue-600">{{ $lecture->questions->count() }}</span>
                            <p class="text-sm text-blue-600">Practice Questions</p>
                        </div>
                        <div class="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4 text-center">
                            <span class="text-2xl font-bold text-purple-600">{{ $lecture->examQuestions->count() }}</span>
                            <p class="text-sm text-purple-600">Exam Questions</p>
                        </div>
                    </div>

                    @if(Auth::check() && Auth::user()->role !== 'student')
                    <div class="mt-6 pt-6 border-t dark:border-gray-700 flex space-x-4 animate-fade-in-up" style="animation-delay: 0.6s;">
                        <a href="{{ route('lectures.edit', $lecture) }}" class="inline-flex items-center px-4 py-2 bg-yellow-500 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-yellow-600 transition ease-in-out duration-150">Edit</a>
                        <form action="{{ route('lectures.destroy', $lecture) }}" method="POST" class="inline">
                            @csrf
                            @method('DELETE')
                            <button type="submit" onclick="return confirm('Are you sure?')" class="inline-flex items-center px-4 py-2 bg-red-600 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-red-700 transition ease-in-out duration-150">Delete</button>
                        </form>
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
            animation: fadeInUp 0.5s ease-out forwards;
            opacity: 0;
        }
    </style>

    @auth
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
                        const span = button.querySelector('span');
                        if (data.is_loved) {
                            button.classList.remove('border-gray-300', 'text-gray-400', 'hover:bg-gray-50');
                            button.classList.add('border-red-300', 'text-red-500', 'bg-red-50');
                            svg.setAttribute('fill', 'currentColor');
                            span.textContent = 'Loved';
                        } else {
                            button.classList.remove('border-red-300', 'text-red-500', 'bg-red-50');
                            button.classList.add('border-gray-300', 'text-gray-400', 'hover:bg-gray-50');
                            svg.setAttribute('fill', 'none');
                            span.textContent = 'Love';
                        }
                    }
                });
        }
    </script>
    @endauth
</x-app-layout>