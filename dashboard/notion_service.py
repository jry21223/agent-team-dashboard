"""
Notion Integration Service
Notion API 集成服务

版本：1.0.0
作者：Jerry (Codex AI Team)
"""

import os
import json
from datetime import datetime
from notion_client import Client
from notion_client.errors import APIResponseError


class NotionService:
    """Notion API 服务类"""
    
    def __init__(self, api_key: str):
        """
        初始化 Notion 客户端
        
        Args:
            api_key: Notion Integration Token
        """
        self.client = Client(auth=api_key)
        self.api_key = api_key
        self.connected = False
        
    def test_connection(self) -> dict:
        """
        测试 Notion 连接
        
        Returns:
            dict: 连接状态和信息
        """
        try:
            # 获取用户信息
            user = self.client.users.me()
            self.connected = True
            return {
                'success': True,
                'connected': True,
                'user': {
                    'name': user.get('name', 'Unknown'),
                    'email': user.get('person', {}).get('email', 'Unknown')
                },
                'workspace': user.get('workspace_name', 'Unknown')
            }
        except APIResponseError as e:
            self.connected = False
            return {
                'success': False,
                'connected': False,
                'error': str(e)
            }
        except Exception as e:
            self.connected = False
            return {
                'success': False,
                'connected': False,
                'error': f"Connection failed: {str(e)}"
            }
    
    def get_user_pages(self, page_size: int = 20) -> list:
        """
        获取用户的页面列表
        
        Args:
            page_size: 每页数量
            
        Returns:
            list: 页面列表
        """
        try:
            response = self.client.search(
                filter={"property": "object", "value": "page"},
                sort={"direction": "descending", "timestamp": "last_edited_time"},
                page_size=page_size
            )
            
            pages = []
            for result in response.get('results', []):
                pages.append({
                    'id': result['id'],
                    'title': self._get_page_title(result),
                    'url': result.get('url', ''),
                    'icon': result.get('icon', None),
                    'cover': result.get('cover', None),
                    'last_edited_time': result.get('last_edited_time', ''),
                    'created_time': result.get('created_time', '')
                })
            
            return pages
        except Exception as e:
            print(f"Error getting pages: {e}")
            return []
    
    def get_databases(self, page_size: int = 20) -> list:
        """
        获取用户的数据库列表
        
        Args:
            page_size: 每页数量
            
        Returns:
            list: 数据库列表
        """
        try:
            response = self.client.search(
                filter={"property": "object", "value": "database"},
                sort={"direction": "descending", "timestamp": "last_edited_time"},
                page_size=page_size
            )
            
            databases = []
            for result in response.get('results', []):
                databases.append({
                    'id': result['id'],
                    'title': self._get_page_title(result),
                    'url': result.get('url', ''),
                    'icon': result.get('icon', None),
                    'description': result.get('description', ''),
                    'last_edited_time': result.get('last_edited_time', '')
                })
            
            return databases
        except Exception as e:
            print(f"Error getting databases: {e}")
            return []
    
    def get_database_items(self, database_id: str, page_size: int = 20) -> list:
        """
        获取数据库中的条目
        
        Args:
            database_id: 数据库 ID
            page_size: 每页数量
            
        Returns:
            list: 数据库条目列表
        """
        try:
            response = self.client.databases.query(
                database_id=database_id,
                page_size=page_size
            )
            
            items = []
            for result in response.get('results', []):
                items.append({
                    'id': result['id'],
                    'name': self._get_page_title(result),
                    'url': result.get('url', ''),
                    'properties': result.get('properties', {}),
                    'created_time': result.get('created_time', ''),
                    'last_edited_time': result.get('last_edited_time', '')
                })
            
            return items
        except Exception as e:
            print(f"Error getting database items: {e}")
            return []
    
    def create_page(self, parent_id: str, title: str, content: str = '') -> dict:
        """
        创建新页面
        
        Args:
            parent_id: 父页面 ID
            title: 页面标题
            content: 页面内容
            
        Returns:
            dict: 创建的页面信息
        """
        try:
            new_page = self.client.pages.create(
                parent={"page_id": parent_id},
                properties={
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": content
                                    }
                                }
                            ]
                        }
                    }
                ] if content else []
            )
            
            return {
                'success': True,
                'page': {
                    'id': new_page['id'],
                    'title': self._get_page_title(new_page),
                    'url': new_page.get('url', '')
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def append_block(self, page_id: str, content: str) -> dict:
        """
        向页面追加内容块
        
        Args:
            page_id: 页面 ID
            content: 内容
            
        Returns:
            dict: 操作结果
        """
        try:
            self.client.blocks.children.append(
                block_id=page_id,
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": content
                                    }
                                }
                            ]
                        }
                    }
                ]
            )
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _get_page_title(self, page: dict) -> str:
        """
        获取页面标题
        
        Args:
            page: 页面对象
            
        Returns:
            str: 页面标题
        """
        properties = page.get('properties', {})
        title_prop = properties.get('title', {})
        
        if title_prop and 'title' in title_prop and len(title_prop['title']) > 0:
            return title_prop['title'][0].get('plain_text', 'Untitled')
        
        return 'Untitled'


# 全局 Notion 服务实例
notion_service = None


def init_notion_service(api_key: str) -> NotionService:
    """
    初始化 Notion 服务
    
    Args:
        api_key: Notion API Key
        
    Returns:
        NotionService: Notion 服务实例
    """
    global notion_service
    notion_service = NotionService(api_key)
    return notion_service


def get_notion_service() -> NotionService:
    """
    获取 Notion 服务实例
    
    Returns:
        NotionService: Notion 服务实例
    """
    return notion_service
