<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Http\Requests\UserRequest;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class UserController extends Controller
{
    public function index(): \Illuminate\Contracts\View\View
    {
        $users = User::latest()->paginate(10);
        return view('users.index', compact('users'));
    }

    public function create(): \Illuminate\Contracts\View\View
    {
        return view('users.create');
    }

    public function store(UserRequest $request): \Illuminate\Http\RedirectResponse
    {
        $data = $request->validated();
        $data['password'] = Hash::make($data['password']);

        User::create($data);
        return redirect()->route('users.index')->with('success', 'User created successfully!');
    }

    public function show(User $user): \Illuminate\Contracts\View\View
    {
        $user->load('teacherPermissions.subject', 'teacherPermissions.lecture');
        return view('users.show', compact('user'));
    }

    public function edit(User $user): \Illuminate\Contracts\View\View
    {
        return view('users.edit', compact('user'));
    }

    public function update(UserRequest $request, User $user): \Illuminate\Http\RedirectResponse
    {
        $data = $request->validated();

        // Only update password if provided
        if (!empty($data['password'])) {
            $data['password'] = Hash::make($data['password']);
        } else {
            unset($data['password']);
        }

        $user->update($data);
        return redirect()->route('users.index')->with('success', 'User updated successfully!');
    }

    public function destroy(User $user): \Illuminate\Http\RedirectResponse
    {
        $user->delete();
        return redirect()->route('users.index')->with('success', 'User deleted successfully!');
    }
}
