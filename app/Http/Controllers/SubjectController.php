<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Http\Requests\SubjectRequest;
use App\Models\Subject;

class SubjectController extends Controller
{
    public function index(): \Illuminate\Contracts\View\View
    {
        $subjects = Subject::latest()->paginate(10);
        return view('subjects.index', compact('subjects'));
    }

    public function create(): \Illuminate\Contracts\View\View
    {
        return view('subjects.create');
    }

    public function store(SubjectRequest $request): \Illuminate\Http\RedirectResponse
    {
        Subject::create($request->validated());
        return redirect()->route('subjects.index')->with('success', 'Subject created successfully!');
    }

    public function show(Subject $subject): \Illuminate\Contracts\View\View
    {
        $subject->load('lectures');
        return view('subjects.show', compact('subject'));
    }

    public function edit(Subject $subject): \Illuminate\Contracts\View\View
    {
        return view('subjects.edit', compact('subject'));
    }

    public function update(SubjectRequest $request, Subject $subject): \Illuminate\Http\RedirectResponse
    {
        $subject->update($request->validated());
        return redirect()->route('subjects.index')->with('success', 'Subject updated successfully!');
    }

    public function destroy(Subject $subject): \Illuminate\Http\RedirectResponse
    {
        $subject->delete();
        return redirect()->route('subjects.index')->with('success', 'Subject deleted successfully!');
    }
}
