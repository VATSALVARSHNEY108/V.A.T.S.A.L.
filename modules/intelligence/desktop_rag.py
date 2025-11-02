"""
🧠 Smart Desktop RAG (Retrieval Augmented Generation)
AI-powered system to interact with all desktop data intelligently
"""

import os
import json
import time
import hashlib
import csv
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict
import mimetypes
import re
from gemini_controller import get_client
from google.genai import types


class DesktopRAG:
    """
    Smart RAG system for desktop data:
    - Index all desktop files and folders
    - Extract text content from various file types
    - Semantic search with AI
    - Answer questions about desktop content
    - Summarize documents and folders
    - Find relevant files intelligently
    """
    
    def __init__(self):
        """Initialize Desktop RAG system"""
        self.index_file = "desktop_index.json"
        self.tags_file = "desktop_tags.json"
        self.relationships_file = "desktop_relationships.json"
        self.timeline_file = "desktop_timeline.json"
        
        self.index = self._load_index()
        self.tags = self._load_tags()
        self.relationships = self._load_relationships()
        self.timeline = self._load_timeline()
        
        self.supported_text_extensions = {
            '.txt', '.md', '.py', '.js', '.html', '.css', '.json', 
            '.csv', '.xml', '.yaml', '.yml', '.log', '.ini', '.cfg',
            '.java', '.cpp', '.c', '.h', '.rs', '.go', '.rb', '.php',
            '.sh', '.bat', '.ps1', '.sql', '.r', '.jsx', '.tsx', '.vue',
            '.ts', '.swift', '.kt', '.scala', '.pl', '.lua', '.vim',
            '.asm', '.toml', '.dockerfile', '.gitignore', '.env'
        }
        
        # Auto-categorization keywords
        self.category_keywords = {
            'code': ['class', 'function', 'def ', 'import', 'const ', 'var ', 'let ', 'public', 'private'],
            'documentation': ['readme', 'doc', 'guide', 'tutorial', 'manual', '# ', '## '],
            'configuration': ['config', 'settings', 'env', '.ini', '.cfg', '.toml'],
            'data': ['csv', 'json', 'xml', 'dataset', 'data'],
            'web': ['html', 'css', 'javascript', 'react', 'vue', 'angular'],
            'database': ['sql', 'query', 'database', 'table', 'select', 'insert'],
            'testing': ['test', 'spec', 'mock', 'assert', 'expect'],
            'build': ['makefile', 'build', 'compile', 'package.json', 'requirements.txt'],
        }
        
        print("🧠 Advanced Desktop RAG initialized")
        print(f"   📊 Indexed files: {len(self.index)}")
        print(f"   🏷️  Tagged files: {sum(len(v) for v in self.tags.values())}")
        print(f"   🔗 File relationships: {len(self.relationships)}")
    
    def _load_index(self) -> Dict:
        """Load existing index from disk"""
        try:
            if os.path.exists(self.index_file):
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load index: {e}")
        return {}
    
    def _load_tags(self) -> Dict:
        """Load tags from disk"""
        try:
            if os.path.exists(self.tags_file):
                with open(self.tags_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def _load_relationships(self) -> Dict:
        """Load file relationships from disk"""
        try:
            if os.path.exists(self.relationships_file):
                with open(self.relationships_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def _load_timeline(self) -> List:
        """Load file timeline from disk"""
        try:
            if os.path.exists(self.timeline_file):
                with open(self.timeline_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def _save_index(self):
        """Save index to disk"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, ensure_ascii=False)
            print(f"✅ Index saved: {len(self.index)} files indexed")
        except Exception as e:
            print(f"❌ Failed to save index: {e}")
    
    def _save_tags(self):
        """Save tags to disk"""
        try:
            with open(self.tags_file, 'w', encoding='utf-8') as f:
                json.dump(self.tags, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Failed to save tags: {e}")
    
    def _save_relationships(self):
        """Save relationships to disk"""
        try:
            with open(self.relationships_file, 'w', encoding='utf-8') as f:
                json.dump(self.relationships, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Failed to save relationships: {e}")
    
    def _save_timeline(self):
        """Save timeline to disk"""
        try:
            with open(self.timeline_file, 'w', encoding='utf-8') as f:
                json.dump(self.timeline, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Failed to save timeline: {e}")
    
    def _extract_text_content(self, file_path: str) -> Optional[str]:
        """Extract text content from various file types"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            # Text-based files
            if file_ext in self.supported_text_extensions:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(50000)  # Limit to 50KB per file
                    return content
            
            # Binary files - just get metadata
            return None
            
        except Exception as e:
            return None
    
    def index_directory(self, directory: str, max_files: int = 1000, 
                       recursive: bool = True) -> Dict:
        """
        Index all files in a directory
        
        Args:
            directory: Path to directory to index
            max_files: Maximum number of files to index
            recursive: Include subdirectories
        """
        print(f"\n🔍 Indexing directory: {directory}")
        print(f"   📁 Recursive: {recursive}")
        print(f"   📊 Max files: {max_files}")
        
        indexed_count = 0
        skipped_count = 0
        start_time = time.time()
        
        try:
            path = Path(directory).expanduser()
            
            if not path.exists():
                return {
                    "success": False,
                    "error": f"Directory not found: {directory}"
                }
            
            # Get file iterator
            if recursive:
                file_iter = path.rglob("*")
            else:
                file_iter = path.glob("*")
            
            for file_path in file_iter:
                if indexed_count >= max_files:
                    print(f"⚠️  Reached max files limit ({max_files})")
                    break
                
                if not file_path.is_file():
                    continue
                
                # Skip hidden files and system files
                if file_path.name.startswith('.') or file_path.name.startswith('~'):
                    skipped_count += 1
                    continue
                
                # Skip very large files (>10MB)
                try:
                    if file_path.stat().st_size > 10 * 1024 * 1024:
                        skipped_count += 1
                        continue
                except:
                    continue
                
                # Extract content and metadata
                file_key = str(file_path.absolute())
                content = self._extract_text_content(str(file_path))
                
                file_stats = file_path.stat()
                
                self.index[file_key] = {
                    "path": str(file_path),
                    "name": file_path.name,
                    "extension": file_path.suffix.lower(),
                    "size": file_stats.st_size,
                    "modified": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                    "created": datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                    "content": content[:5000] if content else None,  # First 5KB
                    "has_content": content is not None,
                    "indexed_at": datetime.now().isoformat()
                }
                
                indexed_count += 1
                
                if indexed_count % 100 == 0:
                    print(f"   📊 Indexed {indexed_count} files...")
            
            # Save index
            self._save_index()
            
            elapsed = time.time() - start_time
            
            return {
                "success": True,
                "indexed_files": indexed_count,
                "skipped_files": skipped_count,
                "total_in_index": len(self.index),
                "time_taken": f"{elapsed:.2f}s",
                "directory": directory
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "indexed_files": indexed_count
            }
    
    def quick_index_common_folders(self) -> Dict:
        """Index common user folders (Desktop, Documents, Downloads)"""
        print("\n🏠 Quick indexing common folders...")
        
        home = Path.home()
        common_folders = [
            home / "Desktop",
            home / "Documents", 
            home / "Downloads",
            home / "Pictures",
            home / "Videos"
        ]
        
        results = []
        total_indexed = 0
        
        for folder in common_folders:
            if folder.exists():
                print(f"\n📂 Indexing {folder.name}...")
                result = self.index_directory(str(folder), max_files=500, recursive=True)
                results.append({
                    "folder": folder.name,
                    "result": result
                })
                if result.get("success"):
                    total_indexed += result.get("indexed_files", 0)
        
        return {
            "success": True,
            "total_files_indexed": total_indexed,
            "folders_indexed": len([r for r in results if r["result"].get("success")]),
            "details": results
        }
    
    def search_files(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search files by name, content, or metadata
        
        Args:
            query: Search query
            max_results: Maximum number of results
        """
        print(f"\n🔍 Searching for: '{query}'")
        
        query_lower = query.lower()
        matches = []
        
        for file_key, file_data in self.index.items():
            score = 0
            
            # Name match
            if query_lower in file_data["name"].lower():
                score += 10
            
            # Extension match
            if query_lower in file_data["extension"]:
                score += 5
            
            # Content match
            if file_data.get("content") and query_lower in file_data["content"].lower():
                score += 20
                
                # Count occurrences
                occurrences = file_data["content"].lower().count(query_lower)
                score += min(occurrences * 2, 20)
            
            if score > 0:
                matches.append({
                    **file_data,
                    "relevance_score": score
                })
        
        # Sort by relevance
        matches.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return matches[:max_results]
    
    def ask_about_files(self, question: str) -> Dict:
        """
        Ask AI a question about your desktop files
        
        Args:
            question: Natural language question about files
        """
        print(f"\n💬 Question: {question}")
        
        # Get relevant files based on keywords
        keywords = question.lower().split()
        relevant_files = []
        
        for file_key, file_data in self.index.items():
            relevance = 0
            
            for keyword in keywords:
                if len(keyword) < 3:
                    continue
                
                if keyword in file_data["name"].lower():
                    relevance += 2
                if file_data.get("content") and keyword in file_data["content"].lower():
                    relevance += 3
            
            if relevance > 0:
                relevant_files.append({
                    "path": file_data["path"],
                    "name": file_data["name"],
                    "size": file_data["size"],
                    "modified": file_data["modified"],
                    "content_preview": file_data.get("content", "")[:500] if file_data.get("content") else "No text content",
                    "relevance": relevance
                })
        
        relevant_files.sort(key=lambda x: x["relevance"], reverse=True)
        top_files = relevant_files[:20]
        
        # Build context for AI
        context = f"Desktop File Index Summary:\n"
        context += f"- Total files indexed: {len(self.index)}\n"
        context += f"- Relevant files found: {len(top_files)}\n\n"
        
        if top_files:
            context += "Most Relevant Files:\n"
            for i, file_info in enumerate(top_files[:10], 1):
                context += f"\n{i}. {file_info['name']}\n"
                context += f"   Path: {file_info['path']}\n"
                context += f"   Size: {file_info['size']} bytes\n"
                context += f"   Modified: {file_info['modified']}\n"
                context += f"   Preview: {file_info['content_preview'][:200]}...\n"
        
        # Ask Gemini
        try:
            client = get_client()
            
            prompt = f"""Based on the user's desktop file index, answer this question:

QUESTION: {question}

DESKTOP FILE CONTEXT:
{context}

Provide a helpful, accurate answer based on the indexed files. If you need more information, suggest what additional indexing or searches might help. Be specific about file names, paths, and content when relevant."""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            answer = response.text
            
            return {
                "success": True,
                "question": question,
                "answer": answer,
                "files_analyzed": len(top_files),
                "relevant_files": [f["path"] for f in top_files[:5]]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "question": question
            }
    
    def summarize_folder(self, folder_path: str) -> Dict:
        """
        AI-powered summary of a folder's contents
        
        Args:
            folder_path: Path to folder to summarize
        """
        print(f"\n📊 Summarizing folder: {folder_path}")
        
        # Get files in this folder
        folder_files = []
        
        for file_key, file_data in self.index.items():
            if folder_path in file_data["path"]:
                folder_files.append(file_data)
        
        if not folder_files:
            return {
                "success": False,
                "error": f"No indexed files found in {folder_path}. Try indexing first."
            }
        
        # Build summary context
        context = f"Folder: {folder_path}\n"
        context += f"Total files: {len(folder_files)}\n\n"
        
        # File types
        extensions = {}
        total_size = 0
        
        for file_data in folder_files:
            ext = file_data["extension"] or "no extension"
            extensions[ext] = extensions.get(ext, 0) + 1
            total_size += file_data["size"]
        
        context += "File Types:\n"
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
            context += f"  {ext}: {count} files\n"
        
        context += f"\nTotal Size: {total_size / (1024*1024):.2f} MB\n\n"
        
        # Sample file names and content
        context += "Sample Files:\n"
        for file_data in folder_files[:20]:
            context += f"  - {file_data['name']}"
            if file_data.get("content"):
                context += f" (Preview: {file_data['content'][:100]}...)"
            context += "\n"
        
        # Ask Gemini to summarize
        try:
            client = get_client()
            
            prompt = f"""Analyze and summarize this folder:

{context}

Provide:
1. Overall purpose/theme of the folder
2. Main file types and what they're for
3. Organization quality (well-organized or messy)
4. Suggestions for better organization
5. Notable files or patterns
6. Potential cleanup opportunities"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            return {
                "success": True,
                "folder": folder_path,
                "file_count": len(folder_files),
                "total_size_mb": f"{total_size / (1024*1024):.2f}",
                "file_types": extensions,
                "summary": response.text
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def find_duplicates_smart(self) -> Dict:
        """Find duplicate files using AI-powered content analysis"""
        print("\n🔍 Finding duplicate files (smart analysis)...")
        
        # Group by name (without extension)
        name_groups = {}
        
        for file_key, file_data in self.index.items():
            name_base = Path(file_data["name"]).stem.lower()
            
            if name_base not in name_groups:
                name_groups[name_base] = []
            
            name_groups[name_base].append(file_data)
        
        # Find potential duplicates
        duplicates = []
        
        for name_base, files in name_groups.items():
            if len(files) > 1:
                # Check if content is similar
                for i, file1 in enumerate(files):
                    for file2 in files[i+1:]:
                        # Same size is a strong indicator
                        if file1["size"] == file2["size"]:
                            duplicates.append({
                                "file1": file1["path"],
                                "file2": file2["path"],
                                "name": name_base,
                                "size": file1["size"],
                                "confidence": "high"
                            })
                        # Similar name
                        elif file1["name"].lower() == file2["name"].lower():
                            duplicates.append({
                                "file1": file1["path"],
                                "file2": file2["path"],
                                "name": name_base,
                                "size_diff": abs(file1["size"] - file2["size"]),
                                "confidence": "medium"
                            })
        
        return {
            "success": True,
            "duplicates_found": len(duplicates),
            "duplicates": duplicates[:50],  # Limit results
            "potential_savings_mb": sum(d.get("size", 0) for d in duplicates) / (1024*1024)
        }
    
    def get_index_stats(self) -> Dict:
        """Get statistics about the current index"""
        if not self.index:
            return {
                "total_files": 0,
                "message": "No files indexed yet. Run quick index first."
            }
        
        extensions = {}
        total_size = 0
        with_content = 0
        
        for file_data in self.index.values():
            ext = file_data["extension"] or "no extension"
            extensions[ext] = extensions.get(ext, 0) + 1
            total_size += file_data["size"]
            if file_data.get("has_content"):
                with_content += 1
        
        return {
            "total_files": len(self.index),
            "files_with_text_content": with_content,
            "total_size_mb": f"{total_size / (1024*1024):.2f}",
            "file_types": dict(sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]),
            "last_updated": max(
                (file_data["indexed_at"] for file_data in self.index.values()),
                default="Never"
            )
        }


    def compute_file_hash(self, file_path: str) -> Optional[str]:
        """Compute MD5 hash of file for exact duplicate detection"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
    
    def find_exact_duplicates(self) -> Dict:
        """Find exact duplicate files using content hashing"""
        print("\n🔍 Finding exact duplicates (hash-based)...")
        
        hash_groups = defaultdict(list)
        
        for file_key, file_data in self.index.items():
            file_hash = self.compute_file_hash(file_data["path"])
            if file_hash:
                hash_groups[file_hash].append(file_data)
        
        duplicates = []
        total_waste = 0
        
        for file_hash, files in hash_groups.items():
            if len(files) > 1:
                group = {
                    "hash": file_hash,
                    "files": [f["path"] for f in files],
                    "size": files[0]["size"],
                    "count": len(files),
                    "waste_mb": (files[0]["size"] * (len(files) - 1)) / (1024*1024)
                }
                duplicates.append(group)
                total_waste += group["waste_mb"]
        
        return {
            "success": True,
            "duplicate_groups": len(duplicates),
            "total_duplicates": sum(d["count"] for d in duplicates),
            "potential_savings_mb": f"{total_waste:.2f}",
            "details": sorted(duplicates, key=lambda x: x["waste_mb"], reverse=True)[:20]
        }
    
    def auto_categorize_files(self) -> Dict:
        """Automatically categorize files based on content analysis"""
        print("\n🏷️  Auto-categorizing files...")
        
        categories = defaultdict(list)
        
        for file_key, file_data in self.index.items():
            file_categories = set()
            content = (file_data.get("content") or "").lower()
            name = file_data["name"].lower()
            
            # Check against category keywords
            for category, keywords in self.category_keywords.items():
                for keyword in keywords:
                    if keyword in content or keyword in name:
                        file_categories.add(category)
                        break
            
            # Auto-detect from extension
            ext = file_data["extension"]
            if ext in ['.py', '.js', '.java', '.cpp', '.c', '.rs', '.go']:
                file_categories.add('code')
            elif ext in ['.md', '.txt', '.pdf', '.doc']:
                file_categories.add('documentation')
            elif ext in ['.jpg', '.png', '.gif', '.svg']:
                file_categories.add('images')
            elif ext in ['.mp4', '.avi', '.mkv', '.mov']:
                file_categories.add('videos')
            elif ext in ['.mp3', '.wav', '.flac']:
                file_categories.add('audio')
            
            for cat in file_categories:
                categories[cat].append(file_data["path"])
        
        return {
            "success": True,
            "categories": {cat: len(files) for cat, files in categories.items()},
            "details": {cat: files[:10] for cat, files in categories.items()}
        }
    
    def add_tags(self, file_paths: List[str], tags: List[str]) -> Dict:
        """Add tags to files"""
        print(f"\n🏷️  Adding tags: {tags}")
        
        tagged_count = 0
        
        for file_path in file_paths:
            if file_path in self.index:
                for tag in tags:
                    if tag not in self.tags:
                        self.tags[tag] = []
                    if file_path not in self.tags[tag]:
                        self.tags[tag].append(file_path)
                        tagged_count += 1
        
        self._save_tags()
        
        return {
            "success": True,
            "files_tagged": len(file_paths),
            "tags_added": tagged_count
        }
    
    def search_by_tags(self, tags: List[str]) -> List[Dict]:
        """Search files by tags"""
        matching_files = set()
        
        for tag in tags:
            if tag in self.tags:
                matching_files.update(self.tags[tag])
        
        results = []
        for file_path in matching_files:
            if file_path in self.index:
                results.append(self.index[file_path])
        
        return results
    
    def analyze_file_relationships(self) -> Dict:
        """Analyze relationships between files (imports, references)"""
        print("\n🔗 Analyzing file relationships...")
        
        relationships = defaultdict(set)
        
        for file_key, file_data in self.index.items():
            content = file_data.get("content", "")
            if not content:
                continue
            
            # Python imports
            if file_data["extension"] == '.py':
                imports = re.findall(r'from\s+(\w+)|import\s+(\w+)', content)
                for match in imports:
                    module = match[0] or match[1]
                    relationships[file_key].add(f"imports:{module}")
            
            # JavaScript imports
            elif file_data["extension"] in ['.js', '.jsx', '.ts', '.tsx']:
                imports = re.findall(r'import.*from\s+[\'"](.+?)[\'"]', content)
                for imp in imports:
                    relationships[file_key].add(f"imports:{imp}")
            
            # File references (any file mentioning another)
            for other_key, other_data in self.index.items():
                if other_key != file_key:
                    if other_data["name"] in content:
                        relationships[file_key].add(f"references:{other_data['name']}")
        
        # Convert sets to lists for JSON
        self.relationships = {k: list(v) for k, v in relationships.items()}
        self._save_relationships()
        
        return {
            "success": True,
            "files_with_relationships": len(self.relationships),
            "total_relationships": sum(len(v) for v in self.relationships.values())
        }
    
    def get_file_timeline(self, days: int = 30) -> Dict:
        """Get timeline of file modifications"""
        print(f"\n📅 Analyzing file timeline (last {days} days)...")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        timeline = defaultdict(list)
        
        for file_key, file_data in self.index.items():
            try:
                mod_date = datetime.fromisoformat(file_data["modified"])
                if mod_date >= cutoff_date:
                    date_key = mod_date.strftime("%Y-%m-%d")
                    timeline[date_key].append({
                        "path": file_data["path"],
                        "name": file_data["name"],
                        "size": file_data["size"],
                        "time": mod_date.strftime("%H:%M:%S")
                    })
            except:
                continue
        
        return {
            "success": True,
            "days_analyzed": days,
            "dates_with_activity": len(timeline),
            "total_changes": sum(len(files) for files in timeline.values()),
            "timeline": dict(sorted(timeline.items(), reverse=True)[:days])
        }
    
    def export_index_to_csv(self, output_file: str = "desktop_index_export.csv") -> Dict:
        """Export index to CSV file"""
        print(f"\n📤 Exporting index to {output_file}...")
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                if not self.index:
                    return {"success": False, "error": "No files indexed"}
                
                fieldnames = ['path', 'name', 'extension', 'size', 'modified', 'created', 'has_content']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for file_data in self.index.values():
                    writer.writerow({
                        'path': file_data['path'],
                        'name': file_data['name'],
                        'extension': file_data['extension'],
                        'size': file_data['size'],
                        'modified': file_data['modified'],
                        'created': file_data['created'],
                        'has_content': file_data.get('has_content', False)
                    })
            
            return {
                "success": True,
                "exported_files": len(self.index),
                "output_file": output_file
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_advanced_analytics(self) -> Dict:
        """Get comprehensive analytics about indexed files"""
        print("\n📊 Generating advanced analytics...")
        
        analytics = {
            "overview": {},
            "size_distribution": {},
            "temporal_patterns": {},
            "file_health": {},
            "recommendations": []
        }
        
        # Overview
        total_size = sum(f["size"] for f in self.index.values())
        analytics["overview"] = {
            "total_files": len(self.index),
            "total_size_mb": f"{total_size / (1024*1024):.2f}",
            "avg_file_size_kb": f"{(total_size / len(self.index) / 1024):.2f}" if self.index else "0",
            "files_with_content": sum(1 for f in self.index.values() if f.get("has_content"))
        }
        
        # Size distribution
        size_ranges = {"<1KB": 0, "1-10KB": 0, "10-100KB": 0, "100KB-1MB": 0, "1-10MB": 0, ">10MB": 0}
        for file_data in self.index.values():
            size_kb = file_data["size"] / 1024
            if size_kb < 1:
                size_ranges["<1KB"] += 1
            elif size_kb < 10:
                size_ranges["1-10KB"] += 1
            elif size_kb < 100:
                size_ranges["10-100KB"] += 1
            elif size_kb < 1024:
                size_ranges["100KB-1MB"] += 1
            elif size_kb < 10240:
                size_ranges["1-10MB"] += 1
            else:
                size_ranges[">10MB"] += 1
        analytics["size_distribution"] = size_ranges
        
        # Temporal patterns
        recent_24h = 0
        recent_week = 0
        recent_month = 0
        now = datetime.now()
        
        for file_data in self.index.values():
            try:
                mod_date = datetime.fromisoformat(file_data["modified"])
                delta = now - mod_date
                if delta.days == 0:
                    recent_24h += 1
                if delta.days < 7:
                    recent_week += 1
                if delta.days < 30:
                    recent_month += 1
            except:
                continue
        
        analytics["temporal_patterns"] = {
            "modified_last_24h": recent_24h,
            "modified_last_week": recent_week,
            "modified_last_month": recent_month
        }
        
        # File health checks
        large_files = [f for f in self.index.values() if f["size"] > 100*1024*1024]
        old_files = []
        for file_data in self.index.values():
            try:
                mod_date = datetime.fromisoformat(file_data["modified"])
                if (now - mod_date).days > 365:
                    old_files.append(file_data)
            except:
                continue
        
        analytics["file_health"] = {
            "files_over_100mb": len(large_files),
            "files_over_1_year_old": len(old_files),
            "largest_file": max(self.index.values(), key=lambda x: x["size"])["name"] if self.index else None
        }
        
        # AI-powered recommendations
        if len(self.index) > 100:
            analytics["recommendations"].append("Consider organizing files into more subdirectories")
        if len(large_files) > 10:
            analytics["recommendations"].append(f"You have {len(large_files)} very large files (>100MB) - consider archiving or compression")
        if len(old_files) > 50:
            analytics["recommendations"].append(f"You have {len(old_files)} files over 1 year old - consider cleanup")
        if recent_24h > 50:
            analytics["recommendations"].append("High file activity detected today - ensure backups are current")
        
        return {
            "success": True,
            "analytics": analytics
        }
    
    def compare_files(self, file1_path: str, file2_path: str) -> Dict:
        """Compare two files and find similarities/differences"""
        print(f"\n🔄 Comparing files...")
        
        if file1_path not in self.index or file2_path not in self.index:
            return {"success": False, "error": "One or both files not in index"}
        
        file1 = self.index[file1_path]
        file2 = self.index[file2_path]
        
        comparison = {
            "files": [file1["name"], file2["name"]],
            "size_difference": abs(file1["size"] - file2["size"]),
            "same_extension": file1["extension"] == file2["extension"],
            "same_size": file1["size"] == file2["size"]
        }
        
        # Content comparison
        if file1.get("content") and file2.get("content"):
            content1 = set(file1["content"].split())
            content2 = set(file2["content"].split())
            common_words = content1.intersection(content2)
            total_words = content1.union(content2)
            
            similarity = len(common_words) / len(total_words) if total_words else 0
            comparison["content_similarity_percent"] = f"{similarity * 100:.1f}"
        
        return {
            "success": True,
            "comparison": comparison
        }
    
    def get_smart_recommendations(self) -> Dict:
        """AI-powered recommendations for file organization and cleanup"""
        print("\n💡 Generating smart recommendations...")
        
        try:
            # Gather insights
            stats = self.get_index_stats()
            duplicates = self.find_duplicates_smart()
            analytics = self.get_advanced_analytics()
            
            context = f"""File System Analysis:
- Total files: {stats['total_files']}
- Total size: {stats['total_size_mb']} MB
- File types: {stats.get('file_types', {})}
- Duplicate files found: {duplicates.get('duplicates_found', 0)}
- Files over 1 year old: {analytics['analytics']['file_health'].get('files_over_1_year_old', 0)}
- Large files (>100MB): {analytics['analytics']['file_health'].get('files_over_100mb', 0)}
"""
            
            client = get_client()
            
            prompt = f"""As a file organization expert, analyze this desktop file system and provide actionable recommendations:

{context}

Provide:
1. Top 3 cleanup opportunities
2. Organization improvement suggestions
3. Storage optimization tips
4. Security concerns (if any)
5. Workflow efficiency improvements

Be specific and practical."""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            return {
                "success": True,
                "recommendations": response.text,
                "based_on": {
                    "total_files": stats['total_files'],
                    "duplicates": duplicates.get('duplicates_found', 0)
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def filter_files(self, 
                    extension: Optional[str] = None,
                    min_size: Optional[int] = None,
                    max_size: Optional[int] = None,
                    modified_after: Optional[str] = None,
                    modified_before: Optional[str] = None,
                    contains_text: Optional[str] = None) -> List[Dict]:
        """Advanced filtering of indexed files"""
        print("\n🔍 Filtering files with advanced criteria...")
        
        results = []
        
        for file_key, file_data in self.index.items():
            # Extension filter
            if extension and file_data["extension"] != extension:
                continue
            
            # Size filters
            if min_size and file_data["size"] < min_size:
                continue
            if max_size and file_data["size"] > max_size:
                continue
            
            # Date filters
            try:
                if modified_after:
                    mod_date = datetime.fromisoformat(file_data["modified"])
                    after_date = datetime.fromisoformat(modified_after)
                    if mod_date < after_date:
                        continue
                
                if modified_before:
                    mod_date = datetime.fromisoformat(file_data["modified"])
                    before_date = datetime.fromisoformat(modified_before)
                    if mod_date > before_date:
                        continue
            except:
                pass
            
            # Text content filter
            if contains_text:
                content = file_data.get("content", "")
                if contains_text.lower() not in content.lower():
                    continue
            
            results.append(file_data)
        
        return results
    
    def backup_index(self, backup_name: Optional[str] = None) -> Dict:
        """Create a backup of the current index"""
        if not backup_name:
            backup_name = f"desktop_index_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            import shutil
            shutil.copy(self.index_file, backup_name)
            return {
                "success": True,
                "backup_file": backup_name,
                "files_backed_up": len(self.index)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


def create_desktop_rag():
    """Factory function to create DesktopRAG instance"""
    return DesktopRAG()


# Example usage
if __name__ == "__main__":
    rag = create_desktop_rag()
    
    print("\n=== Desktop RAG Demo ===\n")
    
    # Index common folders
    result = rag.quick_index_common_folders()
    print(f"\n✅ Indexed {result['total_files_indexed']} files")
    
    # Get stats
    stats = rag.get_index_stats()
    print(f"\n📊 Index Stats:")
    print(f"   Total files: {stats['total_files']}")
    print(f"   Total size: {stats['total_size_mb']} MB")
    
    # Search example
    matches = rag.search_files("python")
    print(f"\n🔍 Found {len(matches)} files matching 'python'")
    
    # Ask question
    answer = rag.ask_about_files("What Python files do I have?")
    if answer["success"]:
        print(f"\n💬 AI Answer:\n{answer['answer']}")
