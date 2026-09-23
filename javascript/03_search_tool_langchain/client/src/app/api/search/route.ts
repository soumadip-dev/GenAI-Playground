import { NextResponse } from 'next/server';

const backendBaseUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8080';

export async function POST(request: Request) {
  try {
    const requestBody = await request.json();

    const backendResponse = await fetch(`${backendBaseUrl}/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    const responseData = await backendResponse.json();

    return NextResponse.json(responseData, {
      status: backendResponse.status,
    });
  } catch (error) {
    console.error('API /search error:', error);

    return NextResponse.json(
      {
        error: 'Failed to communicate with the backend',
      },
      { status: 500 }
    );
  }
}
