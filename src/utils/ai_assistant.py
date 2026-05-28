import re
import json
from typing import List, Dict, Optional, Tuple

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIAssistant:
    def __init__(self, use_real_ai=False, api_key=None, model="gpt-3.5-turbo"):
        self.use_real_ai = use_real_ai
        self.api_key = api_key
        self.model = model
        
        if self.use_real_ai and OPENAI_AVAILABLE and self.api_key:
            openai.api_key = self.api_key
        
        self.supported_commands = {
            'rename': {
                'patterns': [
                    r'(重命名|改名|重命名文件|修改文件名)',
                    r'(批量)?重命名(为)?(.+)',
                    r'把(文件|图片|照片)(的)?名字改成(.+)',
                    r'文件名添加(前缀|后缀)(为)?(.+)',
                ],
                'description': '批量重命名文件',
                'params': ['prefix', 'suffix', 'start_number']
            },
            'convert': {
                'patterns': [
                    r'(转换|格式转换|图片转换)',
                    r'(把|将)(图片|照片)(转换|改成)(成)?(jpg|jpeg|png|webp)',
                    r'(jpg|jpeg|png|webp)(转|转换)(成)?(jpg|jpeg|png|webp)',
                ],
                'description': '图片格式转换',
                'params': ['to_format']
            },
            'compress': {
                'patterns': [
                    r'(压缩|打包|zip)',
                    r'(把|将)(文件|文件夹)(压缩|打包)(成)?(zip)',
                    r'创建(压缩包|zip包)',
                ],
                'description': '文件压缩',
                'params': ['output']
            },
            'classify': {
                'patterns': [
                    r'(分类|整理|归类)',
                    r'(按|根据)(扩展名|类型|日期)(分类|整理)',
                    r'整理(文件|图片)',
                ],
                'description': '文件分类',
                'params': ['by_type']
            },
            'watermark': {
                'patterns': [
                    r'(水印|加水印)',
                    r'(给|为)(图片|照片)(添加|加上)(水印|文字水印)',
                    r'(图片|照片)(加|添加)(水印)',
                ],
                'description': '图片加水印',
                'params': ['type', 'content']
            },
            'exif': {
                'patterns': [
                    r'(exif|元数据|照片信息|图片信息)',
                    r'(提取|获取)(图片|照片)(的)?(exif|信息|元数据)',
                    r'(导出|保存)(exif|照片信息)',
                ],
                'description': '提取EXIF信息',
                'params': []
            },
            'copy': {
                'patterns': [
                    r'(复制|拷贝)',
                    r'(把|将)(文件|图片)(复制|拷贝)(到)?(.+)',
                    r'复制(文件|图片)',
                ],
                'description': '批量复制文件',
                'params': ['target_dir']
            },
            'move': {
                'patterns': [
                    r'(移动|转移)',
                    r'(把|将)(文件|图片)(移动|转移)(到)?(.+)',
                    r'移动(文件|图片)',
                ],
                'description': '批量移动文件',
                'params': ['target_dir']
            },
            'modify_time': {
                'patterns': [
                    r'(修改时间|改时间|文件时间)',
                    r'(把|将)(文件|图片)(的)?(创建时间|修改时间)(改成|设为)(.+)',
                    r'(修改|设置)(文件|图片)(时间)',
                ],
                'description': '批量修改文件时间',
                'params': ['create_time', 'modify_time']
            }
        }

    def parse_command(self, user_input: str) -> Optional[Dict]:
        """解析用户自然语言命令"""
        user_input = user_input.strip()
        
        if self.use_real_ai and OPENAI_AVAILABLE and self.api_key:
            return self._parse_with_real_ai(user_input)
        else:
            return self._parse_with_rules(user_input)

    def _parse_with_rules(self, user_input: str) -> Optional[Dict]:
        """使用规则匹配解析命令"""
        for command_type, config in self.supported_commands.items():
            for pattern in config['patterns']:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    result = {
                        'command': command_type,
                        'description': config['description'],
                        'params': {}
                    }
                    result['params'] = self._extract_params(command_type, user_input)
                    return result
        
        return None

    def _parse_with_real_ai(self, user_input: str) -> Optional[Dict]:
        """使用真正的AI引擎解析命令"""
        try:
            prompt = self._build_prompt(user_input)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个文件处理助手，擅长理解用户的文件操作需求并转换为结构化命令。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            result = response.choices[0].message['content'].strip()
            
            try:
                parsed = json.loads(result)
                return parsed
            except json.JSONDecodeError:
                return self._parse_with_rules(user_input)
                
        except Exception as e:
            print(f"AI解析失败，使用规则匹配: {e}")
            return self._parse_with_rules(user_input)

    def _build_prompt(self, user_input: str) -> str:
        """构建AI提示词"""
        commands_info = "\n".join([
            f"- {cmd}: {config['description']}" 
            for cmd, config in self.supported_commands.items()
        ])
        
        prompt = f"""
用户输入: "{user_input}"

请分析用户的意图，识别出用户想要执行的文件操作命令。

支持的命令类型:
{commands_info}

请以JSON格式输出，包含以下字段:
- command: 命令类型（必须是上述支持的命令之一）
- description: 命令描述
- params: 参数对象（根据命令类型添加必要参数）

如果无法识别命令，请返回: {{"command": null, "description": "无法识别", "params": {{}}}}

示例输出:
{{"command": "convert", "description": "图片格式转换", "params": {{"to_format": "webp"}}}}
{{"command": "rename", "description": "批量重命名文件", "params": {{"prefix": "vacation_", "suffix": "_2024"}}}}
{{"command": "watermark", "description": "图片加水印", "params": {{"type": "text", "content": "版权所有"}}}}
"""
        return prompt

    def _extract_params(self, command_type: str, user_input: str) -> Dict:
        """从命令中提取参数"""
        params = {}
        
        if command_type == 'convert':
            formats = ['jpg', 'jpeg', 'png', 'webp']
            for fmt in formats:
                if fmt.lower() in user_input.lower():
                    params['to_format'] = fmt.lower()
                    break
        
        elif command_type == 'rename':
            if '前缀' in user_input:
                match = re.search(r'前缀(为)?(.+)', user_input)
                if match:
                    params['prefix'] = match.group(2).strip()
            if '后缀' in user_input:
                match = re.search(r'后缀(为)?(.+)', user_input)
                if match:
                    params['suffix'] = match.group(2).strip()
        
        elif command_type == 'watermark':
            if '文字' in user_input or '文字水印' in user_input:
                params['type'] = 'text'
                match = re.search(r'(水印|文字)(为)?(.+)', user_input)
                if match:
                    params['content'] = match.group(3).strip()
            else:
                params['type'] = 'text'
                params['content'] = '© 水印'
        
        elif command_type in ['copy', 'move']:
            match = re.search(r'(到|目标|保存到)(.+)', user_input)
            if match:
                params['target_dir'] = match.group(2).strip()
        
        elif command_type == 'classify':
            if '日期' in user_input:
                params['by_type'] = 'date'
            else:
                params['by_type'] = 'extension'
        
        return params

    def get_supported_commands(self) -> List[Dict]:
        """获取所有支持的命令"""
        return [
            {
                'command': cmd,
                'description': config['description'],
                'examples': self._get_examples(cmd)
            }
            for cmd, config in self.supported_commands.items()
        ]

    def _get_examples(self, command_type: str) -> List[str]:
        """获取命令示例"""
        examples = {
            'rename': [
                '把这些文件重命名',
                '文件名添加前缀"vacation_"',
                '批量重命名为"photo_001"格式'
            ],
            'convert': [
                '把图片转换成webp格式',
                'jpg转png',
                '图片格式转换'
            ],
            'compress': [
                '压缩这些文件',
                '创建zip压缩包',
                '打包文件'
            ],
            'classify': [
                '按扩展名分类文件',
                '根据日期整理图片',
                '整理文件'
            ],
            'watermark': [
                '给图片加水印',
                '添加文字水印"我的照片"',
                '图片加版权水印'
            ],
            'exif': [
                '提取图片EXIF信息',
                '获取照片元数据',
                '导出图片信息'
            ],
            'copy': [
                '复制文件到桌面',
                '拷贝图片到新文件夹',
                '批量复制文件'
            ],
            'move': [
                '移动文件到新目录',
                '转移图片到备份文件夹',
                '批量移动文件'
            ],
            'modify_time': [
                '修改文件创建时间',
                '设置文件修改时间',
                '批量改时间'
            ]
        }
        return examples.get(command_type, [])

    def generate_response(self, user_input: str) -> Tuple[Optional[Dict], str]:
        """生成响应"""
        parsed = self.parse_command(user_input)
        
        if parsed and parsed.get('command'):
            return parsed, f'我来帮您{parsed["description"]}！'
        else:
            return None, '抱歉，我不太理解您的意思。您可以尝试说：\n- 把图片转换成webp格式\n- 给图片加水印\n- 按扩展名分类文件\n- 提取图片EXIF信息'

    def is_real_ai_available(self) -> bool:
        """检查是否可以使用真实AI"""
        return self.use_real_ai and OPENAI_AVAILABLE and self.api_key is not None
