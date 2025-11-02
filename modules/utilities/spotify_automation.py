 return {"success": True, "message": "⏮️ Previous track"}
        return result
    
    def set_volume(self, volume_percent):
        """Set volume (0-100)"""
        volume = max(0, min(100, int(volume_percent)))
        result = self._make_spotify_request(f'me/player/volume?volume_percent={volume}', 'PUT')
        if result.get('success'):
            return {"success": True, "message": f"🔊 Volume set to {volume}%"}
        return result
    
    def get_current_track(self):
        """Get currently playing track info"""
        result = self._make_spotify_request('me/player/currently-playing')
        if result.get('success'):
            data = result.get('data', {})
            if not data or not data.get('item'):
                return {"success": True, "message": "No track currently playing"}
            
            item = data['item']
            artists = ', '.join([artist['name'] for artist in item.get('artists', [])])
            track_name = item.get('name', 'Unknown')
            album = item.get('album', {}).get('name', 'Unknown')
            is_playing = data.get('is_playing', False)
            
            status = "▶️ Playing" if is_playing else "⏸️ Paused"
            message = f"{status}: {track_name} by {artists}\nAlbum: {album}"
            
            return {
                "success": True,
                "message": message,
                "track_info": {
                    "name": track_name,
                    "artists": artists,
                    "album": album,
                    "is_playing": is_playing,
                    "uri": item.get('uri')
                }
            }
        return result
    
    def search(self, query, search_type='track', limit=5):
        """Search Spotify (track/artist/album/playlist)"""
        from urllib.parse import quote
        encoded_query = quote(query)
        endpoint = f'search?q={encoded_query}&type={search_type}&limit={limit}'
        
        result = self._make_spotify_request(endpoint)
        if result.get('success'):
            data = result.get('data', {})
            items = data.get(f'{search_type}s', {}).get('items', [])
            
            if not items:
                return {"success": True, "message": f"No {search_type}s found for '{query}'"}
            
            results_list = []
            for item in items:
                if search_type == 'track':
                    artists = ', '.join([a['name'] for a in item.get('artists', [])])
                    results_list.append({
                        "name": item['name'],
                        "artists": artists,
                        "uri": item['uri'],
                        "display": f"{item['name']} - {artists}"
                    })
                elif search_type == 'artist':
                    results_list.append({
                        "name": item['name'],
                        "uri": item['uri'],
                        "display": item['name']
                    })
                elif search_type == 'playlist':
                    results_list.append({
                        "name": item['name'],
                        "owner": item.get('owner', {}).get('display_name', 'Unknown'),
                        "uri": item['uri'],
                        "display": f"{item['name']} (by {item.get('owner', {}).get('display_name', 'Unknown')})"
                    })
                elif search_type == 'album':
                    artists = ', '.join([a['name'] for a in item.get('artists', [])])
                    results_list.append({
                        "name": item['name'],
                        "artists": artists,
                        "uri": item['uri'],
                        "display": f"{item['name']} - {artists}"
                    })
            
            message = f"🔍 Found {len(results_list)} {search_type}(s):\n"
            for i, item in enumerate(results_list, 1):
                message += f"  {i}. {item['display']}\n"
            
            return {
                "success": True,
                "message": message.strip(),
                "results": results_list
            }
        return result
    
    def play_track(self, query):
        """Search and play first matching track"""
        search_result = self.search(query, 'track', 1)
        
        # Check if search failed at API level
        if not search_result.get('success'):
            return {
                "success": False,
                "message": f"Spotify search failed: {search_result.get('message', 'Unknown error')}"
            }
        
        # Check if results were found
        if search_result.get('results'):
            track = search_result['results'][0]
            play_result = self.play(track['uri'])
            if play_result.get('success'):
                return {
                    "success": True,
                    "message": f"🎵 Playing: {track['display']}"
                }
            return play_result
        
        # No results found
        return {"success": False, "message": f"Track '{query}' not found on Spotify. Try being more specific or check the spelling."}
    
    def get_playlists(self, limit=20):
        """Get user's playlists"""
        result = self._make_spotify_request(f'me/playlists?limit={limit}')
        if result.get('success'):
            data = result.get('data', {})
            items = data.get('items', [])
            
            if not items:
                return {"success": True, "message": "No playlists found"}
            
            playlists = []
            message = f"📚 Your playlists ({len(items)}):\n"
            for i, item in enumerate(items, 1):
                playlists.append({
                    "name": item['name'],
                    "tracks": item.get('tracks', {}).get('total', 0),
                    "uri": item['uri']
                })
                message += f"  {i}. {item['name']} ({item.get('tracks', {}).get('total', 0)} tracks)\n"
            
            return {
                "success": True,
                "message": message.strip(),
                "playlists": playlists
            }
        return result
    
    def shuffle(self, state=True):
        """Toggle shuffle on/off"""
        state_str = 'true' if state else 'false'
        result = self._make_spotify_request(f'me/player/shuffle?state={state_str}', 'PUT')
        if result.get('success'):
            status = "on" if state else "off"
            return {"success": True, "message": f"🔀 Shuffle {status}"}
        return result
    
    def repeat(self, state='context'):
        """Set repeat mode: track, context (playlist/album), or off"""
        result = self._make_spotify_request(f'me/player/repeat?state={state}', 'PUT')
        if result.get('success'):
            modes = {'track': 'one track', 'context': 'playlist/album', 'off': 'off'}
            return {"success": True, "message": f"🔁 Repeat {modes.get(state, state)}"}
        return result


def create_spotify_automation():
    """Factory function to create SpotifyAutomation instance"""
    return SpotifyAutomation()
