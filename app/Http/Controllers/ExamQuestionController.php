<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Http\Requests\ExamQuestionRequest;
use App\Models\ExamQuestion;
use App\Models\Lecture;
use Illuminate\Support\Facades\Storage;

class ExamQuestionController extends Controller
{
    public function index(): \Illuminate\Contracts\View\View
    {
        $examQuestions = ExamQuestion::with('lecture.subject')->latest()->paginate(10);
        return view('exam_questions.index', compact('examQuestions'));
    }

    public function create(): \Illuminate\Contracts\View\View
    {
        $lectures = Lecture::with('subject')->orderBy('title')->get();
        return view('exam_questions.create', compact('lectures'));
    }

    public function store(ExamQuestionRequest $request): \Illuminate\Http\RedirectResponse
    {
        $data = $request->validated();

        // Handle image uploads
        if ($request->hasFile('question_image')) {
            $data['question_image'] = $request->file('question_image')->store('exam_questions/images', 'public');
        }
        if ($request->hasFile('solution_image')) {
            $data['solution_image'] = $request->file('solution_image')->store('exam_questions/solutions', 'public');
        }

        ExamQuestion::create($data);
        return redirect()->route('exam_questions.index')->with('success', 'Exam Question created successfully!');
    }

    public function show(ExamQuestion $examQuestion): \Illuminate\Contracts\View\View
    {
        $examQuestion->load('lecture.subject');
        return view('exam_questions.show', compact('examQuestion'));
    }

    public function edit(ExamQuestion $examQuestion): \Illuminate\Contracts\View\View
    {
        $lectures = Lecture::with('subject')->orderBy('title')->get();
        return view('exam_questions.edit', compact('examQuestion', 'lectures'));
    }

    public function update(ExamQuestionRequest $request, ExamQuestion $examQuestion): \Illuminate\Http\RedirectResponse
    {
        $data = $request->validated();

        // Handle image uploads
        if ($request->hasFile('question_image')) {
            if ($examQuestion->question_image) {
                Storage::disk('public')->delete($examQuestion->question_image);
            }
            $data['question_image'] = $request->file('question_image')->store('exam_questions/images', 'public');
        }
        if ($request->hasFile('solution_image')) {
            if ($examQuestion->solution_image) {
                Storage::disk('public')->delete($examQuestion->solution_image);
            }
            $data['solution_image'] = $request->file('solution_image')->store('exam_questions/solutions', 'public');
        }

        $examQuestion->update($data);
        return redirect()->route('exam_questions.index')->with('success', 'Exam Question updated successfully!');
    }

    public function destroy(ExamQuestion $examQuestion): \Illuminate\Http\RedirectResponse
    {
        // Delete images if exist
        if ($examQuestion->question_image) {
            Storage::disk('public')->delete($examQuestion->question_image);
        }
        if ($examQuestion->solution_image) {
            Storage::disk('public')->delete($examQuestion->solution_image);
        }

        $examQuestion->delete();
        return redirect()->route('exam_questions.index')->with('success', 'Exam Question deleted successfully!');
    }
}
