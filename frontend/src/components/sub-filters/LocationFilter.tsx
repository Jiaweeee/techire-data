import { useState, useEffect, useRef } from "react";
import { Search } from "lucide-react";
import { SearchParams } from "../../types/api";
import { getLocations } from "../../services/api";

// Location Filter Component
export function LocationFilter({
  params,
  onFilterChange,
}: {
  params: SearchParams;
  onFilterChange: (params: Partial<SearchParams>) => void;
}) {
  const [search, setSearch] = useState("");
  const [locations, setLocations] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function fetchLocations() {
      try {
        const data = await getLocations();
        setLocations(data.sort((a, b) => a.localeCompare(b)));
      } catch (error) {
        console.error("Failed to fetch locations:", error);
        setLocations([]);
      }
    }
    fetchLocations();
  }, []);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const filteredLocations = locations.filter((location) =>
    location.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="border-t border-gray-200 pt-4">
      <h3 className="font-semibold text-gray-900 mb-2">Locations</h3>
      <div className="space-y-2">
        <div className="relative" ref={dropdownRef}>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onFocus={() => setIsOpen(true)}
            placeholder="Search locations..."
            className="w-full px-3 py-2 border rounded-lg text-sm"
          />
          <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />

          {isOpen && filteredLocations.length > 0 && (
            <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
              {filteredLocations.map((location) => (
                <div
                  key={location}
                  className="px-4 py-2 hover:bg-gray-100 cursor-pointer text-sm text-gray-700"
                  onClick={() => {
                    if (!params.locations?.includes(location)) {
                      const newLocations = [
                        ...(params.locations || []),
                        location,
                      ];
                      onFilterChange({ locations: newLocations });
                    }
                    setIsOpen(false);
                  }}
                >
                  {location}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}