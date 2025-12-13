<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Http\Requests\SectionRequest;
use App\Models\Section;
use App\Models\Lecture;

class SectionController extends Controller
{
    public function index(): \Illuminate\Contracts\View\View
    {
        $sections = Section::with('lecture.subject')->latest()->paginate(10);
        return view('sections.index', compact('sections'));
    }

    public function create(): \Illuminate\Contracts\View\View
    {
        $lectures = Lecture::with('subject')->orderBy('title')->get();
        return view('sections.create', compact('lectures'));
    }

    public function store(SectionRequest $request): \Illuminate\Http\RedirectResponse
    {
        Section::create($request->validated());
        return redirect()->route('sections.index')->with('success', 'Section created successfully!');
    }

    public function show(Section $section): \Illuminate\Contracts\View\View
    {
        $section->load('lecture.subject');
        return view('sections.show', compact('section'));
    }

    public function edit(Section $section): \Illuminate\Contracts\View\View
    {
        $lectures = Lecture::with('subject')->orderBy('title')->get();
        return view('sections.edit', compact('section', 'lectures'));
    }

    public function update(SectionRequest $request, Section $section): \Illuminate\Http\RedirectResponse
    {
        $section->update($request->validated());
        return redirect()->route('sections.index')->with('success', 'Section updated successfully!');
    }

    public function destroy(Section $section): \Illuminate\Http\RedirectResponse
    {
        $section->delete();
        return redirect()->route('sections.index')->with('success', 'Section deleted successfully!');
    }
}
