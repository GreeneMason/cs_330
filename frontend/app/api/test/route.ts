import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({ 
    message: 'Test endpoint working',
    timestamp: new Date().toISOString(),
    cwd: process.cwd()
  });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    console.log('Test POST received:', body);
    
    return NextResponse.json({
      success: true,
      message: 'Test POST working',
      received: body
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Test POST failed', details: String(error) },
      { status: 500 }
    );
  }
}