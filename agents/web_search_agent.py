"""
WebSearchAgent - Searches the web for algorithm hints and similar problems
Uses DuckDuckGo API (free, unlimited) to find relevant competitive programming resources
"""

from typing import List, Dict, Optional
import re
from ddgs import DDGS


class WebSearchAgent:
    """
    Agent that searches the web for algorithm hints, similar problems, and competitive programming resources.
    Helps the optimal agent by providing context from educational sites and competitive programming platforms.
    """
    
    def __init__(self):
        self.ddgs = DDGS()
        self.target_domains = [
            'codeforces.com',
            'leetcode.com',
            'geeksforgeeks.org',
            'cp-algorithms.com',
            'usaco.guide',
            'stackoverflow.com',
            'atcoder.jp',
            'topcoder.com',
            'hackerrank.com',
            'codechef.com'
        ]
    
    def search_algorithm_hints(self, problem_statement: str, max_results: int = 5) -> List[Dict]:
        """
        Main entry point: searches for algorithm hints based on problem statement.
        
        Args:
            problem_statement: The problem description text
            max_results: Maximum number of search results to return
        
        Returns:
            List of search results with title, link, snippet, and relevance score
        """
        try:
            # Generate search query from problem
            query = self._generate_query(problem_statement)
            
            # Perform DuckDuckGo search
            raw_results = self._search_duckduckgo(query, max_results * 2)  # Get more, filter later
            
            # Filter and rank results
            filtered_results = self._filter_results(raw_results, problem_statement)
            
            return filtered_results[:max_results]
        
        except Exception as e:
            print(f"[WebSearchAgent] Error during search: {e}")
            return []
    
    def _generate_query(self, problem_statement: str) -> str:
        """
        Generate a search query from the problem statement.
        Extracts key algorithmic terms and adds domain filters.
        
        Args:
            problem_statement: Raw problem text
        
        Returns:
            Optimized search query string
        """
        # Common competitive programming keywords
        algo_keywords = [
            'dynamic programming', 'dp', 'greedy', 'binary search', 'bfs', 'dfs',
            'graph', 'tree', 'segment tree', 'fenwick tree', 'trie', 'dijkstra',
            'floyd warshall', 'bellman ford', 'kruskal', 'prim', 'topological sort',
            'backtracking', 'divide and conquer', 'sliding window', 'two pointers',
            'prefix sum', 'suffix array', 'lca', 'disjoint set', 'union find',
            'knapsack', 'longest common subsequence', 'lcs', 'longest increasing subsequence',
            'lis', 'matrix exponentiation', 'bit manipulation', 'combinatorics',
            'number theory', 'modular arithmetic', 'prime', 'gcd', 'lcm'
        ]
        
        # Extract keywords from problem
        problem_lower = problem_statement.lower()
        found_keywords = []
        
        for keyword in algo_keywords:
            if keyword in problem_lower:
                found_keywords.append(keyword)
        
        # Extract potential problem-specific terms (words in title or repeated words)
        words = re.findall(r'\b[a-z]{4,}\b', problem_lower)
        word_freq = {}
        for word in words:
            if word not in ['input', 'output', 'sample', 'example', 'given', 'find', 'calculate']:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top 3 most frequent words
        frequent_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        problem_terms = [word for word, _ in frequent_words]
        
        # Build query
        if found_keywords:
            # Prefer algorithmic keywords
            query_parts = found_keywords[:2] + problem_terms[:1]
        else:
            # Use problem terms + competitive programming hint
            query_parts = problem_terms[:2] + ['algorithm', 'competitive programming']
        
        query = ' '.join(query_parts)
        
        # Add site filter for better results
        site_filter = ' OR '.join([f'site:{domain}' for domain in self.target_domains[:3]])
        full_query = f"{query} ({site_filter})"
        
        return full_query
    
    def _search_duckduckgo(self, query: str, max_results: int) -> List[Dict]:
        """
        Perform DuckDuckGo search using duckduckgo-search library.
        
        Args:
            query: Search query string
            max_results: Maximum number of results
        
        Returns:
            List of raw search results
        """
        try:
            results = []
            # Use text search
            search_results = self.ddgs.text(query, max_results=max_results)
            
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'link': result.get('href', ''),
                    'snippet': result.get('body', ''),
                    'source': result.get('href', '').split('/')[2] if result.get('href') else ''
                })
            
            return results
        
        except Exception as e:
            print(f"[WebSearchAgent] DuckDuckGo search error: {e}")
            return []
    
    def _filter_results(self, results: List[Dict], problem_statement: str) -> List[Dict]:
        """
        Filter and rank search results by relevance.
        Prioritizes results from trusted domains and with matching keywords.
        
        Args:
            results: Raw search results
            problem_statement: Original problem for relevance scoring
        
        Returns:
            Filtered and sorted results with relevance scores
        """
        if not results:
            return []
        
        # Extract problem keywords for relevance scoring
        problem_lower = problem_statement.lower()
        problem_words = set(re.findall(r'\b[a-z]{4,}\b', problem_lower))
        
        scored_results = []
        for result in results:
            score = 0
            
            # Domain scoring (trusted competitive programming sites)
            source = result.get('source', '').lower()
            for domain in self.target_domains:
                if domain in source:
                    score += 10
                    break
            
            # Keyword matching in title/snippet
            title_lower = result.get('title', '').lower()
            snippet_lower = result.get('snippet', '').lower()
            
            for word in problem_words:
                if word in title_lower:
                    score += 3
                if word in snippet_lower:
                    score += 1
            
            # Bonus for algorithm keywords
            algo_indicators = [
                'algorithm', 'solution', 'approach', 'complexity', 'time complexity',
                'space complexity', 'optimal', 'efficient', 'tutorial', 'explanation'
            ]
            for indicator in algo_indicators:
                if indicator in title_lower or indicator in snippet_lower:
                    score += 2
            
            result['relevance_score'] = score
            scored_results.append(result)
        
        # Sort by relevance score
        scored_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return scored_results
    
    def extract_hints(self, search_results: List[Dict]) -> str:
        """
        Format search results into hint text for the optimal agent.
        
        Args:
            search_results: Filtered search results
        
        Returns:
            Formatted hint string
        """
        if not search_results:
            return "No relevant algorithm hints found from web search."
        
        hint_text = "\n=== Algorithm Hints from Web Search ===\n\n"
        hint_text += "The following resources may help with solving this problem:\n\n"
        
        for i, result in enumerate(search_results[:3], 1):  # Top 3 results
            hint_text += f"{i}. {result['title']}\n"
            hint_text += f"   Source: {result['source']}\n"
            hint_text += f"   Link: {result['link']}\n"
            hint_text += f"   Snippet: {result['snippet'][:200]}...\n"
            hint_text += f"   Relevance Score: {result.get('relevance_score', 0)}\n\n"
        
        hint_text += "Consider these algorithmic approaches when designing your solution.\n"
        hint_text += "=" * 50 + "\n"
        
        return hint_text


# Convenience function for quick usage
def search_for_hints(problem_statement: str, max_results: int = 5) -> str:
    """
    Quick function to search and get formatted hints.
    
    Args:
        problem_statement: Problem description
        max_results: Maximum results to return
    
    Returns:
        Formatted hint string
    """
    agent = WebSearchAgent()
    results = agent.search_algorithm_hints(problem_statement, max_results)
    return agent.extract_hints(results)
