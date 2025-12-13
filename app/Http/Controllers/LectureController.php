<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Http\Requests\LectureRequest;
use App\Models\Lecture;
use App\Models\Subject;
use Illuminate\Support\Facades\Storage;

class LectureController extends Controller
{
    public function index(): \Illuminate\Contracts\View\View
    {
        $lectures = Lecture::with('subject')->latest()->paginate(10);
        return view('lectures.index', compact('lectures'));
    }

    public function create(): \Illuminate\Contracts\View\View
    {
        $subjects = Subject::orderBy('name')->get();
        return view('lectures.create', compact('subjects'));
    }

    public function store(LectureRequest $request): \Illuminate\Http\RedirectResponse
    {
        $data = $request->validated();

        // Handle PDF upload
        if ($request->hasFile('pdf_path')) {
            $data['pdf_path'] = $request->file('pdf_path')->store('lectures/pdfs', 'public');
        }

        Lecture::create($data);
        return redirect()->route('lectures.index')->with('success', 'Lecture created successfully!');
    }

    public function show(Lecture $lecture): \Illuminate\Contracts\View\View
    {
        $lecture->load(['subject', 'sections', 'questions', 'examQuestions']);
        return view('lectures.show', compact('lecture'));
    }

    public function edit(Lecture $lecture): \Illuminate\Contracts\View\View
    {
        $subjects = Subject::orderBy('name')->get();
        return view('lectures.edit', compact('lecture', 'subjects'));
    }

    public function update(LectureRequest $request, Lecture $lecture): \Illuminate\Http\RedirectResponse
    {
        $data = $request->validated();

        // Handle PDF upload
        if ($request->hasFile('pdf_path')) {
            // Delete old file if exists
            if ($lecture->pdf_path) {
                Storage::disk('public')->delete($lecture->pdf_path);
            }
            $data['pdf_path'] = $request->file('pdf_path')->store('lectures/pdfs', 'public');
        }

        $lecture->update($data);
        return redirect()->route('lectures.index')->with('success', 'Lecture updated successfully!');
    }

    public function destroy(Lecture $lecture): \Illuminate\Http\RedirectResponse
    {
        // Delete PDF file if exists
        if ($lecture->pdf_path) {
            Storage::disk('public')->delete($lecture->pdf_path);
        }

        $lecture->delete();
        return redirect()->route('lectures.index')->with('success', 'Lecture deleted successfully!');
    }
}
