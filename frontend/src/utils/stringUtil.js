/**
 * Some string utility
 */

/**
 * Return initial from string
 * @param {string} name
 * @returns {string}
 */
export function getInitial(name, separate='') {
  if (!name) {
    return '';
  }
  if (name.length <= 2) {
    return name.toUpperCase();
  }
  const parts = name.trim().split(' ');
  const initials = [];
  const length = parts.length;

  if (length > 0) {
    const first = parts[0] || ' ';
    initials.push(first[0].toUpperCase());
  }
  if (length > 1) {
    const last = parts[length - 1] || ' ';
    initials.push(last[0].toUpperCase());
  }

  return initials.join(separate);
}


const latPattern = '(\\+|-)?(?:90(?:(?:\\.0{1,9})?)|(?:[0-9]|[1-8][0-9])(?:(?:\\.[0-9]{1,9})?))';
const lngPattern = '(\\+|-)?(?:180(?:(?:\\.0{1,9})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\\.[0-9]{1,9})?))';
const latLngRegex = new RegExp(`^${latPattern}\\s?[,]\\s?${lngPattern}$`);

/**
 * Check if given query has the form of lat, lng
 * @param {string} query
 * @returns {Boolean} true if query is lat,lng form, false otherwise
 */
export function isLatLngPair(query) {
  return latLngRegex.test(query);
}