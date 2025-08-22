import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

export async function GET() {
  try {
    // 读取26_Full.txt文件
    const filePath = path.join(process.cwd(), '..', '26_Full.txt');
    
    // 检查文件是否存在
    if (!fs.existsSync(filePath)) {
      return NextResponse.json(
        { error: '数据文件不存在' },
        { status: 404 }
      );
    }

    // 读取文件内容
    const content = fs.readFileSync(filePath, 'utf-8');
    
    return new NextResponse(content, {
      headers: {
        'Content-Type': 'text/plain; charset=utf-8'
      }
    });
  } catch (error) {
    console.error('读取数据文件失败:', error);
    return NextResponse.json(
      { error: '读取数据文件失败' },
      { status: 500 }
    );
  }
}