<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Http\Requests\QuestionRequest;
use App\Models\Question;
use App\Models\Lecture;
use Illuminate\Support\Facades\Storage;

class QuestionController extends Controller
{
    public function index(): \Illuminate\Contracts\View\View
    {
        $questions = Question::with('lecture.subject')->latest()->paginate(10);
        return view('questions.index', compact('questions'));
    }

    public function create(): \Illuminate\Contracts\View\View
    {
        $lectures = Lecture::with('subject')->orderBy('title')->get();
        return view('questions.create', compact('lectures'));
    }

    public function store(QuestionRequest $request): \Illuminate\Http\RedirectResponse
    {
        $data = $request->validated();

        // Handle image uploads
        if ($request->hasFile('question_image')) {
            $data['question_image'] = $request->file('question_image')->store('questions/images', 'public');
        }
        if ($request->hasFile('solution_image')) {
            $data['solution_image'] = $request->file('solution_image')->store('questions/solutions', 'public');
        }

        Question::create($data);
        return redirect()->route('questions.index')->with('success', 'Question created successfully!');
    }

    public function show(Question $question): \Illuminate\Contracts\View\View
    {
        $question->load('lecture.subject');
        return view('questions.show', compact('question'));
    }

    public function edit(Question $question): \Illuminate\Contracts\View\View
    {
        $lectures = Lecture::with('subject')->orderBy('title')->get();
        return view('questions.edit', compact('question', 'lectures'));
    }

    public function update(QuestionRequest $request, Question $question): \Illuminate\Http\RedirectResponse
    {
        $data = $request->validated();

        // Handle image uploads
        if ($request->hasFile('question_image')) {
            if ($question->question_image) {
                Storage::disk('public')->delete($question->question_image);
            }
            $data['question_image'] = $request->file('question_image')->store('questions/images', 'public');
        }
        if ($request->hasFile('solution_image')) {
            if ($question->solution_image) {
                Storage::disk('public')->delete($question->solution_image);
            }
            $data['solution_image'] = $request->file('solution_image')->store('questions/solutions', 'public');
        }

        $question->update($data);
        return redirect()->route('questions.index')->with('success', 'Question updated successfully!');
    }

    public function destroy(Question $question): \Illuminate\Http\RedirectResponse
    {
        // Delete images if exist
        if ($question->question_image) {
            Storage::disk('public')->delete($question->question_image);
        }
        if ($question->solution_image) {
            Storage::disk('public')->delete($question->solution_image);
        }

        $question->delete();
        return redirect()->route('questions.index')->with('success', 'Question deleted successfully!');
    }
}
